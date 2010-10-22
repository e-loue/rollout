# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from optparse import make_option


def findtarget(option, opt_str, value, parser, *args, **kwargs):
    "We only want to specify one target per feature at a time."
    if type(value) == "int":
        delattr(parser.values, 'rollout_group')
        delattr(parser.values, 'rollout_user')
    else:
        delattr(parser.values, 'rollout_percentage')
        if "rollout_group" in parser.values:
            delattr(parser.values, 'rollout_user')


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
            action='callback', callback=findtarget,
            dest='rollout_group', default='',
            help="Activate given group."
        ),
        make_option('-p', '--percentage',
            type='int',
            action='callback', callback=findtarget,
            dest='rollout_percentage', default=0,
            help="Activate given percentage of users."
        ),
        make_option('-u', '--user',
            type='string',
            action='callback', callback=findtarget,
            dest='rollout_user', default='',
            help="Activate given user."
        ),
    )

    help = "Rollout a feature and activate/deactivate a subset of users to use."
    args = 'feature'

    def handle(self, feature='', *args, **options):
        from django.conf import settings
        try:
            from redis import Redis
            from proclaim import Proclaim
        except ImportError:
            raise CommandError("Depends on Proclaim and Redis.")

        if args:
            raise CommandError('Usage is proclaim %s' % self.args)
        if not feature:
            raise CommandError('Usage is proclaim %s' % self.args)

        REDIS_HOST = getattr(settings, "PROCLAIM_HOST", "localhost")
        REDIS_PORT = getattr(settings, "PROCLAIM_PORT", 6379)
        REDIS_DB = getattr(settings, "PROCLAIM_DB", 0)

        proclaim = Proclaim(Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB))

        #if getattr(options, 'rollout_deactivate'):
