#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

VERSION = 0.2

setup(
    name="rollout",
    version=VERSION,
    description="Use Proclaim to release features to target users inside your Django project.",
    long_description="""Conditionally roll out features with Redis by assigning
    percentages, groups or users to features.""",
    author="Timothée Peignier",
    license="MIT",
    author_email="timothee.peignier@tryphon.org",
    url="http://github.com/e-loue/rollout",
    download_url="http://github.com/e-loue/rollout/downloads",
    packages = find_packages(),
    install_requires = ['distribute', 'redis', 'proclaim', 'django'],
    tests_require=['pyyaml'],
    keywords="redis rollout proclaim django",
    classifiers = [
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development"
    ]
)
