import unittest
from base64 import b64encode
from datetime import datetime
from hashlib import sha1
from rackspaceapps import RackspaceApps


class TestRackspaceApps(unittest.TestCase):

    def setUp(self):
        self.test_user_key = 'test'
        self.test_secret_key = 'test'
        self.rsa = RackspaceApps(user_key=self.test_user_key,
                                 secret_key=self.test_secret_key)

    def test_domain_funcs(self):
        domain_funcs = ('list_domains', 'add_domain', 'edit_domain',
                        'delete_domain')
        for func_name in domain_funcs:
            func = getattr(self.rsa, func_name)
            self.assertTrue(callable(func))
