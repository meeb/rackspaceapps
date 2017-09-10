import unittest
from rackspaceapps import RackspaceApps


class TestRackspaceApps(unittest.TestCase):

    def setUp(self):
        self.test_user_key = 'test'
        self.test_secret_key = 'test'
        self.rsa = RackspaceApps(user_key=self.test_user_key,
                                 secret_key=self.test_secret_key)

    def test_rsemail_funcs(self):
        rsemail_funcs = ('list_rsemail', 'add_rsemail', 'edit_rsemail',
                         'delete_rsemail')
        for func_name in rsemail_funcs:
            func = getattr(self.rsa, func_name)
            self.assertTrue(callable(func))
