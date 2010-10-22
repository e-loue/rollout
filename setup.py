#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

VERSION = 0.1

setup(
    name="rollout",
    version=VERSION,
    description="Use Proclaim to release features to target users inside your Django project.",
    long_description="""Conditionally roll out features with Redis by assigning
    percentages, groups or users to features.""",
    author="Timothée Peignier",
    license="MIT",
    author_email="timothee.peignier@tryphon.org",
    url="http://github.com/e-loue/proclaim",
    download_url="http://github.com/e-loue/proclaim/downloads",
    packages = find_packages(),
    install_requires = ['distribute', 'redis', 'proclaim', 'django'],
    tests_require=['pyyaml'],
    keywords="redis rollout proclaim django",
    classifiers = [
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Web Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independant",
        "Topic :: Software Development"
    ]
)
