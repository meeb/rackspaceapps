from requests.exceptions import RequestException


class RackspaceAppsError(RequestException):
    '''
        Base exception.
    '''
    pass


class UnexpectedStatusError(RackspaceAppsError):
    '''
        Raised when the API returns an unexpected response code.
    '''
    pass


class InvalidParameterError(RackspaceAppsError):
    '''
        Raised when a request is made with invalid paramters.
    '''
    pass
