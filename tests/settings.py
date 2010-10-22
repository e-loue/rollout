# -*- coding: utf-8 -*-
DATABASE_ENGINE = 'sqlite3'
ROOT_URLCONF = ''
SITE_ID = 1
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'rollout',
)
TEMPLATE_LOADERS = (
    'django.template.loaders.app_directories.Loader',
)