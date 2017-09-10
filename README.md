# rackspaceapps
Python library for the Rackspace Email &amp; Apps API

This is a partially implemented Python client for the Rackspace Email and Apps
(or "Cloud Office") suite of services. These cover Rackspace email, hosted
Exchange, Sharepoint and related services.

These are some of the older Rackspace services and are not related or included
under the Rackspace Cloud services (servers, databases etc. based on
OpenStack).

API reference documentation for the Rackspace Email and Apps services:

http://api-wiki.apps.rackspace.com/api-wiki/index.php?title=Rest_API

**Note:** We have only implemented the services we need so far, although adding
additional functionality should be trivial if you need it.

## Methods

```python
RackspaceApps.list_domains()
RackspaceApps.add_domain(domain_name='example.com')
RackspaceApps.edit_domain(domain_name='example.com', params={})
RackspaceApps.delete_domain(domain_name='example.com')

RackspaceApps.list_mailboxes(domain_name='example.com')
```

## Synopsis

```python
from rackspaceapps import RackspaceApps


user_key = 'some user key'
secret_key = 'some secret key'
account_number = 'some account number'


rsa = RackspaceApps(user_key=user_key, secret_key=secret_key,
                    account_number=account_number)


domains = rsa.list_domains()
for domain in domains:
        domain_name = domain.get('name')
        mailboxes = rsa.list_rsemail(domain_name=domain_name)
        for mailbox in mailboxes:
            print(domain_name, mailbox)
```
