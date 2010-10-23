# -*- coding: utf-8 -*-
from django.conf import settings
from proclaim import Proclaim
from redis import Redis

REDIS_HOST = getattr(settings, "PROCLAIM_HOST", "localhost")
REDIS_PORT = getattr(settings, "PROCLAIM_PORT", 6379)
REDIS_DB = getattr(settings, "PROCLAIM_DB", 0)

def get_rollout():
    return Proclaim(Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB))

rollout = get_rollout()
