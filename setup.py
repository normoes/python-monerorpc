#!/usr/bin/env python

from setuptools import setup

setup(
    name='python-monerorpc',
    version='0.5.4',
    description='Enhanced version of python-jsonrpc for Monero (monerod, monero-wallet-rpc).',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Norman Moeschter-Schenck',
    author_email='<norman.moeschter@gmail.com>',
    maintainer='Norman Moeschter-Schenck',
    maintainer_email='<norman.moeschter@gmail.com>',
    url='https://www.github.com/monero-ecosystem/python-monerorpc',
    download_url='https://github.com/monero-ecosystem/python-monerorpc/archive/0.5.4.tar.gz',
    packages=['monerorpc'],
    install_requires=[
        'requests',
    ],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 2.7'
    ]
)
