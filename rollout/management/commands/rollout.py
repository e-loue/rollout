# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from optparse import OptionValueError, make_option


def check_target(option, opt_str, value, parser):
    """We only want to specify one target per action."""
    TARGET_OPTS = ['-g', '-p', '-u']
    TARGET_OPTS.remove(opt_str)
    for target in TARGET_OPTS:
        dest = parser.get_option(target).dest
        if getattr(parser.values, dest, True):
            raise OptionValueError("you should not specify several targets")
        if hasattr(parser.values, dest):
            delattr(parser.values, dest)
    setattr(parser.values, option.dest, value)

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--activate',
            action='store_true',
            dest='rollout_activate',
            help="Activate given target for feature."
        ),
        make_option('--deactivate',
            action='store_false',
            dest='rollout_activate',
            help="Deactivate given target for feature."
        ),
        make_option('-g', '--group',
            type='string',
            action='callback', callback=check_target,
            dest='rollout_group', default='',
            help="Activate given group."
        ),
        make_option('-p', '--percentage',
            type='int',
            action='callback', callback=check_target,
            dest='rollout_percentage', default=0,
            help="Activate given percentage of users."
        ),
        make_option('-u', '--user',
            type='string',
            action='callback', callback=check_target,
            dest='rollout_user', default='',
            help="Activate given user."
        ),
    )

    help = "Rollout a feature and activate/deactivate a subset of users to use."
    args = 'feature'

    def handle(self, feature=None, *args, **options):
        from django.conf import settings
        from django.contrib.auth.models import User, Group
        try:
            from redis import Redis
            from proclaim import Proclaim
        except ImportError:
            raise CommandError("Depends on Proclaim and Redis.")

        if not feature:
            raise CommandError('You need to specify a feature name')

        REDIS_HOST = getattr(settings, "PROCLAIM_HOST", "localhost")
        REDIS_PORT = getattr(settings, "PROCLAIM_PORT", 6379)
        REDIS_DB = getattr(settings, "PROCLAIM_DB", 0)

        proclaim = Proclaim(Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB))
        
        if options['rollout_activate']:
            if 'rollout_percentage' in options:
                proclaim.activate_percentage(feature, options['rollout_percentage'])
            if 'rollout_user' in options:
                user = User.objects.get(username=options['rollout_user'])
                proclaim.activate_user(feature, user)
            if 'rollout_group' in options:
                group = Group.objects.get(name=options['rollout_group'])
                proclaim.define_group(group.name, group.user_set.iterator())
                proclaim.activate_group(feature, group.name)
        else:
            if 'rollout_percentage' in options:
                proclaim.deactivate_percentage(feature, options['rollout_percentage'])
            if 'rollout_user' in options:
                user = User.objects.get(username=options['rollout_user'])
                proclaim.deactivate_user(feature, user)
            if 'rollout_group' in options:
                group = Group.objects.get(name=options['rollout_group'])
                proclaim.define_group(group.name, group.user_set.iterator())
                proclaim.deactivate_group(feature, group.name)
    
    
