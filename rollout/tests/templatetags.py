# -*- coding: utf-8 -*-
from django.contrib.auth.models import AnonymousUser, User
from django.template import Context, Template
from django.test import TestCase

from redis import Redis
from proclaim import Proclaim


class TemplateTagTest(TestCase):
    fixtures = ['users']
    
    def setUp(self):
        self.proclaim = Proclaim(Redis())
        self.active_user = User.objects.get(username="elmo")
        self.proclaim.activate_user("newfeature", self.active_user)
        self.inactive_user = User.objects.get(username="abby")
        self.proclaim.deactivate_user("newfeature", self.inactive_user)
    
    def test_anonymous_user(self):
        t = Template("""{% load rollout %}
        {% rollout newfeature %}
            You should not see this feature.
        {% endrollout %}""")
        context = Context({
            'user': AnonymousUser()
        })
        content = t.render(context)
        self.assertTrue("feature" not in content)
    
    def test_inactive_user(self):
        t = Template("""{% load rollout %}
        {% rollout newfeature %}
          You should not see this feature.
        {% endrollout %}
        """)
        context = Context({
            'user': self.inactive_user
        })
        content = t.render(context)
        self.assertTrue("feature" not in content)
    
    def test_active_user(self):
        t = Template("""{% load rollout %}
        {% rollout "newfeature" %}
          You should not see this feature.
        {% endrollout %}
        """)
        context = Context({
            'user': self.active_user
        })
        content = t.render(context)
        self.assertTrue("feature" in content)
    
    def test_active_user_with_template(self):
        t = Template("""{% load rollout %}
        {% rollout newfeature "newfeature.html" %}""")
        context = Context({
            'user': self.active_user
        })
        content = t.render(context)
        self.assertTrue("feature" in content)
    
    def test_inactive_user_with_template(self):
        t = Template("""{% load rollout %}
        {% rollout newfeature "newfeature.html" %}""")
        context = Context({
            'user': self.inactive_user
        })
        content = t.render(context)
        self.assertTrue("feature" not in content)
    
    def test_anonymous_user_with_template(self):
        t = Template("""{% load rollout %}
        {% rollout newfeature "newfeature.html" %}""")
        context = Context({
            'user': AnonymousUser()
        })
        content = t.render(context)
        self.assertTrue("feature" not in content)
    
    def tearDown(self):
        self.proclaim.deactivate_all("newfeature")
    
