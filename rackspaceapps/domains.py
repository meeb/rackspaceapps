from .errors import UnexpectedStatusError, InvalidParameterError


domain_param_casts = {
    'serviceType': str,
    'exchangeExtraStorage': int,
    'exchangeMaxNumMailboxes': int,
    'rsEmailProduct': str,
    'rsEmailBaseMailboxSize': int,
    'rsEmailMaxNumberMailboxes': int,
    'rsEmailExtraStorage': int,
    'blackBerryMobileServiceEnabled': bool,
    'blackBerryLicenses': int,
    'activeSyncMobileServiceEnabled': bool,
    'activeSyncLicenses': int,
    'archivingServiceEnabled': bool,
}
domain_param_strs = {
    'serviceType': ('rsemail', 'exchange', 'both'),
    'rsEmailProduct': ('rse-basic', 'rse-plus'),
}
domain_defaults = {
    # rackspace email
    'serviceType': 'rsemail',
    # no mailboxes
    'rsEmailMaxNumberMailboxes': 0,
    # 10GB default mailbox size
    'rsEmailBaseMailboxSize': 10000,
}


def validate_params(params):
    for param_key, param_value in params.items():
        cast = domain_param_casts.get(param_key)
        if not cast:
            err = 'Invalid parameter: {}'
            raise InvalidParameterError(err.format(param_key))
        try:
            param_value = cast(param_value)
        except ValueError as e:
            err = 'Unable to cast parameter: {} into a: {}'
            raise InvalidParameterError(err.format(param_key, cast)) from e
        if cast == str:
            valid_values = domain_param_strs.get(param_key, '')
            if param_value not in valid_values:
                err = 'Parameter: {} has invalid value: {}'
                raise InvalidParameterError(err.format(param_key, param_value))
        params[param_key] = param_value
    return params


def list_domains(api):

    session = api.build_session()

    def request():
        resource = ('domains',)
        url = api.build_resource(resource)
        per_page = 100
        current_page = 0
        offset = 0
        domains = []
        page_domains = True
        while page_domains:
            query = {'size': per_page, 'offset': offset}
            response = session.get(url, params=query)
            try:
                data = response.json()
            except (ValueError, TypeError):
                data = {}
            if response.status_code != 200:
                err = 'Expected 200, got: {} ({})'
                raise UnexpectedStatusError(err.format(response.status_code,
                                                       response.text))
            total = data.get('total', 0)
            page_domains = data.get('domains', [])
            domains = domains + page_domains
            if offset + per_page > total:
                break
            current_page += 1
            offset = current_page * per_page
        return domains

    return request


def add_domain(api):

    session = api.build_session()

    def request(domain_name='', account_number='', params={}):
        if not account_number:
            account_number = api._account_number
        for k, v in domain_defaults.items():
            if k not in params:
                params[k] = v
        resource = ('customers', account_number, 'domains', domain_name)
        url = api.build_resource(resource)
        params = validate_params(params)
        response = session.post(url, data=params)
        try:
            data = response.json()
        except (ValueError, TypeError):
            data = {}
        if response.status_code != 200:
            err = 'Expected 200, got: {} ({})'
            raise UnexpectedStatusError(err.format(response.status_code,
                                                   response.text))
        return data

    return request


def edit_domain(api):

    session = api.build_session()

    def request(domain_name='', account_number='', params={}):
        if not account_number:
            account_number = api._account_number
        resource = ('customers', account_number, 'domains', domain_name)
        url = api.build_resource(resource)
        response = session.put(url, data=params)
        try:
            data = response.json()
        except (ValueError, TypeError):
            data = {}
        if response.status_code != 200:
            err = 'Expected 200, got: {} ({})'
            raise UnexpectedStatusError(err.format(response.status_code,
                                                   response.text))
        return data

    return request


def delete_domain(api):

    session = api.build_session()

    def request(domain_name='', account_number=''):
        if not account_number:
            account_number = api._account_number
        resource = ('customers', account_number, 'domains', domain_name)
        url = api.build_resource(resource)
        response = session.delete(url)
        try:
            data = response.json()
        except (ValueError, TypeError):
            data = {}
        if response.status_code != 200:
            err = 'Expected 200, got: {} ({})'
            raise UnexpectedStatusError(err.format(response.status_code,
                                                   response.text))
        return data

    return request
