from .errors import UnexpectedStatusError, InvalidParameterError


def list_rsemail(api):

    session = api.build_session()

    def request(domain_name='', account_number=''):
        if not account_number:
            account_number = api._account_number
        resource = ('customers', account_number, 'domains', domain_name, 'rs',
                    'mailboxes')
        url = api.build_resource(resource)
        per_page = 100
        current_page = 0
        offset = 0
        mailboxes = []
        page_mailboxes = True
        while page_mailboxes:
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
            page_mailboxes = data.get('rsMailboxes', [])
            mailboxes = mailboxes + page_mailboxes
            if offset + per_page > total:
                break
            current_page += 1
            offset = current_page * per_page
        return mailboxes

    return request


def add_rsemail(api):

    session = api.build_session()

    def request():
        return {}

    return request


def edit_rsemail(api):

    session = api.build_session()

    def request():
        return {}

    return request


def delete_rsemail(api):

    session = api.build_session()

    def request():
        return {}

    return request
