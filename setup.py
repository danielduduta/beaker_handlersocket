#!/usr/bin/env python
import multiprocessing

from setuptools import setup, find_packages

setup(
    name = 'beaker_handlersocket',
    version = '0.1',
    description = 'Beaker backend to write sessions to MySQL using HandlerSocket.',
    long_description = '\n' + open('README.rst').read(),
    author='Daniel Gavrila',
    author_email = 'danielduduta@gmail.com',
    keywords = 'handlersocket beaker session',
    license = 'New BSD License',
    url = 'https://github.com/danielduduta/beaker_handlersocket/',
    tests_require = ['nose', 'webtest'],
    test_suite='nose.collector',
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Other Environment',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Database',
        'Topic :: Utilities',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    include_package_data=True,
    zip_safe = True,
    entry_points="""
    [beaker.backends]
    handlersocket = beaker_handlersocket:HandlerSocketMySQLNamespaceManager    
    """,
    install_requires=[
        'beaker>=1.6.4'
    ]
)
