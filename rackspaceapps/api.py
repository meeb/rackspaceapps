from urllib.parse import urlunsplit
from base64 import b64encode
from datetime import datetime
from hashlib import sha1
import requests
from requests.exceptions import RequestException


class RackspaceAppsError(Exception):
    pass


class RackspaceApps:

    API_SCHEME = 'https'
    API_NETLOC = 'api.emailsrvr.com'
    API_VERSION = 'v1'
    USER_AGENT = 'rackspaceapps Python API client'
    METHOD_GET = 'get'
    METHOD_PUT = 'put'
    METHOD_POST = 'post'
    METHOD_DELETE = 'delete'
    METHODS = (METHOD_GET, METHOD_PUT, METHOD_POST, METHOD_DELETE)

    def __init__(self, user_key='', secret_key=''):
        self._user_key = str(user_key)
        self._secret_key = str(secret_key)

    def _build_resource(self, resource):
        if not isinstance(resource, (list, tuple)):
            err = 'resource must be a list or a tuple, got: {}'
            raise RackspaceAppsError(err.format(type(resource)))
        uri = '{}/{}'.format(self.API_VERSION, '/'.join(resource))
        return urlunsplit((self.API_SCHEME, self.API_NETLOC, uri, '', ''))

    def _build_signature(self):
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        data = self._user_key.encode()
        data += self.USER_AGENT.encode()
        data += timestamp.encode()
        data += self._secret_key.encode()
        signature = b64encode(sha1(data).digest()).decode()
        return '{}:{}:{}'.format(self._user_key, timestamp, signature)

    def _build_session(self):
        session = requests.Session()
        session.headers.update({'X-Api-Signature': self._build_signature(),
                                'User-Agent': self.USER_AGENT,
                                'Accept': 'application/json'})
        return session

    def _request(self, resource):
        '''
            This is a fancy wrapper for requests.method(...) calls which limits
            the available methods, handles the non-URI format resource and
            pre-populates the session with the authentication headers.
        '''
        session = self._build_session()
        url = self._build_resource(resource)

        def resource_wrapper(method):
            requests_func = getattr(session, method)

            def resource_inner_wrapper():
                try:
                    response = requests_func(url)
                    if response.status_code == 200:
                        return response
                    else:
                        remote = response.headers.get('X-Error-Message', '???')
                        err = 'Error making a "{}" request to: {} ({} / {})'
                        err = err.format(method, url, response.status_code,
                                         remote)
                        raise RackspaceAppsError(err)
                except RequestException as e:
                    err = 'Error making a "{}" request to: {}'
                    raise RackspaceAppsError(err.format(method, url)) from e

            return resource_inner_wrapper

        def requests_wrapper():
            pass

        rtn = requests_wrapper
        for method in self.METHODS:
            setattr(rtn, method, resource_wrapper(method))
        return rtn
