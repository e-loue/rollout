# -*- coding: utf-8 -*-
from StringIO import StringIO

from django.test import TestCase
from django.core import management

class RollOutCommandTest(TestCase):
    fixtures = ['groups', 'users']
    
    def test_activate_percentage(self):
        management.call_command('rollout', 'newfeature', rollout_activate=True, rollout_percentage=20)
    
    def test_deactivate_percentage(self):
        management.call_command('rollout', 'newfeature', rollout_activate=False, rollout_percentage=20)

    def test_activate_user(self):
        management.call_command('rollout', 'newfeature', rollout_activate=True, rollout_user="elmo")
    
    def test_deactivate_user(self):
        management.call_command('rollout', 'newfeature', rollout_activate=False, rollout_user="elmo")
    
    def test_activate_group(self):
        management.call_command('rollout', 'newfeature', rollout_activate=True, rollout_group="Sesame Street")
    
    def test_deactivate_group(self):
        management.call_command('rollout', 'newfeature', rollout_activate=False, rollout_group="Sesame Street")
    

