from setuptools import setup, find_packages
from rackspaceapps import __version__ as version


setup(
    name='rackspaceapps',
    version=str(version),
    url='https://github.com/mgrp/rackspaceapps',
    download_url='https://github.com/mgrp/rackspaceapps/tarball/0.1',
    author='the m group, https://m.pr/',
    author_email='hi@m.pr',
    description=('Python library for the Rackspace Email & Apps API.'),
    license='BSD 3-Clause',
    include_package_data=True,
    install_requires=('requests',),
    packages=find_packages(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords=('rackspace', 'email', 'apps', 'cloud', 'office'),
    test_suite='tests',
)
