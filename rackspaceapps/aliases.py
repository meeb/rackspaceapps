from .errors import UnexpectedStatusError, InvalidParameterError


def list_aliases(api):

    session = api.build_session()

    def request(domain_name='', account_number=''):
        if not account_number:
            account_number = api._account_number
        resource = ('customers', account_number, 'domains', domain_name, 'rs',
                    'aliases')
        url = api.build_resource(resource)
        per_page = 100
        current_page = 0
        offset = 0
        aliases = []
        page_aliases = True
        while page_aliases:
            query = {'size': per_page, 'offset': offset}
            response = session.get(url, params=query)
            try:
                data = response.json()
            except (ValueError, TypeError):
                data = {}
            print(data)
            if response.status_code != 200:
                err = 'Expected 200, got: {} ({})'
                raise UnexpectedStatusError(err.format(response.status_code,
                                                       response.text))
            total = data.get('total', 0)
            page_aliases = data.get('rsMailboxes', [])
            aliases = aliases + page_aliases
            if offset + per_page > total:
                break
            current_page += 1
            offset = current_page * per_page
        return aliases

    return request


def add_alias(api):

    session = api.build_session()

    def request():
        # not implemented yet / not needed
        return {}

    return request


def edit_alias(api):

    session = api.build_session()

    def request():
        # not implemented yet / not needed
        return {}

    return request


def delete_alias(api):

    session = api.build_session()

    def request():
        # not implemented yet / not needed
        return {}

    return request
