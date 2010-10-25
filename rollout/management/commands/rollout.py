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
        from django.contrib.auth.models import User, Group
        from ... import rollout as proclaim
        
        if not feature:
            raise CommandError('You need to specify a feature name')

        if options['rollout_activate']:
            if 'rollout_percentage' in options and options['rollout_percentage']:
                proclaim.activate_percentage(feature, options['rollout_percentage'])
            if 'rollout_user' in options and options['rollout_user']:
                usernames = options['rollout_user'].split(',')
                for user in User.objects.filter(username__in=usernames):
                    proclaim.activate_user(feature, user)
            if 'rollout_group' in options and options['rollout_group']:
                groups = options['rollout_group'].split(',')
                for group in Group.objects.filter(name__in=groups):
                    proclaim.define_group(group.name, *group.user_set.all())
                    proclaim.active_group(feature, group.name)
        else:
            if 'rollout_percentage' in options and options['rollout_percentage']:
                proclaim.deactivate_percentage(feature, options['rollout_percentage'])
            if 'rollout_user' in options and options['rollout_user']:
                usernames = options['rollout_user'].split(',')
                for user in User.objects.filter(username__in=usernames):
                    proclaim.deactivate_user(feature, user)
            if 'rollout_group' in options and options['rollout_group']:
                groups = options['rollout_group'].split(',')
                for group in Group.objects.filter(name__in=groups):
                    proclaim.define_group(group.name, *group.user_set.all())
                    proclaim.deactivate_group(feature, group.name)
    
    
