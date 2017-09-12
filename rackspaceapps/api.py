from urllib.parse import urlunsplit
from base64 import b64encode
from datetime import datetime
from hashlib import sha1
import requests
from requests.exceptions import RequestException
from . import domains, rsemail, aliases


class RackspaceAppsError(Exception):
    pass


class RackspaceApps:

    API_SCHEME = 'https'
    API_NETLOC = 'api.emailsrvr.com'
    API_VERSION = 'v1'
    USER_AGENT = 'rackspaceapps Python API client'

    def __init__(self, user_key='', secret_key='', account_number=''):
        self._user_key = str(user_key)
        self._secret_key = str(secret_key)
        self._account_number = str(account_number)
        self._bootstrap()

    def _bootstrap(self):
        # domain methods
        self.list_domains = domains.list_domains(self)
        self.add_domain = domains.add_domain(self)
        self.edit_domain = domains.edit_domain(self)
        self.delete_domain = domains.delete_domain(self)
        # rsemail methods
        self.list_rsemail = rsemail.list_rsemail(self)
        self.add_rsemail = rsemail.add_rsemail(self)
        self.edit_rsemail = rsemail.edit_rsemail(self)
        self.delete_rsemail = rsemail.delete_rsemail(self)
        # alias methods
        self.list_aliases = aliases.list_aliases(self)
        self.show_alias = aliases.show_alias(self)
        self.add_alias = aliases.add_alias(self)
        self.edit_alias = aliases.edit_alias(self)
        self.delete_alias = aliases.delete_alias(self)

    def build_resource(self, resource):
        if not isinstance(resource, (list, tuple)):
            err = 'resource must be a list or a tuple, got: {}'
            raise RackspaceAppsError(err.format(type(resource)))
        uri = '{}/{}'.format(self.API_VERSION, '/'.join(resource))
        return urlunsplit((self.API_SCHEME, self.API_NETLOC, uri, '', ''))

    def build_signature(self):
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        data = self._user_key.encode()
        data += self.USER_AGENT.encode()
        data += timestamp.encode()
        data += self._secret_key.encode()
        signature = b64encode(sha1(data).digest()).decode()
        return '{}:{}:{}'.format(self._user_key, timestamp, signature)

    def build_session(self):
        session = requests.Session()
        session.headers.update({'X-Api-Signature': self.build_signature(),
                                'User-Agent': self.USER_AGENT,
                                'Accept': 'application/json'})
        return session
