import unittest
from rackspaceapps import RackspaceApps


class TestRackspaceApps(unittest.TestCase):

    def setUp(self):
        self.test_user_key = 'test'
        self.test_secret_key = 'test'
        self.rsa = RackspaceApps(user_key=self.test_user_key,
                                 secret_key=self.test_secret_key)

    def test_rsemail_funcs(self):
        alias_funcs = ('list_aliases', 'add_alias', 'edit_alias',
                       'delete_alias')
        for func_name in alias_funcs:
            func = getattr(self.rsa, func_name)
            self.assertTrue(callable(func))
