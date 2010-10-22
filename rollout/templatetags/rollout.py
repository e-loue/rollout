# -*- coding: utf-8 -*-
from django.conf import settings
from django.template import Library, Variable, TemplateSyntaxError, Node
from django.template.loader import render_to_string

from redis import Redis
from proclaim import Proclaim

REDIS_HOST = getattr(settings, "PROCLAIM_HOST", "localhost")
REDIS_PORT = getattr(settings, "PROCLAIM_PORT", 6379)
REDIS_DB = getattr(settings, "PROCLAIM_DB", 0)

register = Library()


class RollOutNode(Node):
    def __init__(self, feature, nodelist=Node(), template=None):
        self.feature = feature
        self.template = template
        self.nodelist = nodelist
        self.proclaim = Proclaim(Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB))

    def render(self, context):
        feature = self.feature.replace('"', '')
        user = Variable('user').resolve(context)
        if not user.is_authenticated():
            return ''
        is_active = self.proclaim.is_active(feature, user)
        if is_active:
            if self.template:
                template = self.template.replace('"', '')
                try:
                    return render_to_string(template, context)
                except TemplateSyntaxError:
                    return ''  # Fail silently for invalid included templates.
            else:
                return self.nodelist.render(context)
        return ''


@register.tag
def rollout(parser, token):
    """
    Outputs the contents of the block if the currently authenticated user
    is activated to view the feature.

    Examples::

        {% proclaim "newfeature" %}
            ...
        {% endproclaim %}

        {% proclaim "newfeature" "features/gold.html" %}

    """
    tokens = token.split_contents()
    if len(tokens) > 3 or len(tokens) < 1:
        raise TemplateSyntaxError("%r takes one or two arguments" % tokens[0])
    if len(tokens) == 2:
        tag_name, feature = tokens
        end_tag = 'end' + tag_name
        nodelist = parser.parse((end_tag,))
        parser.delete_first_token()
        return RollOutNode(feature, nodelist=nodelist)
    else:
        tag_name, feature, template = tokens
        return RollOutNode(feature, template=template)
