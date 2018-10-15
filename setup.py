#!/usr/bin/env python

from setuptools import setup

setup(name='python-monerorpc',
      version='0.5.1',
      description='Enhanced version of python-jsonrpc for Monero (monerod, monero-wallet-rpc).',
      long_description=open('README.md').read(),
      long_description_content_type='text/markdown',
      author='Norman Moeschter-Schenck',
      author_email='<norman.moeschter@gmail.com>',
      maintainer='Norman Moeschter-Schenck',
      maintainer_email='<norman.moeschter@gmail.com>',
      url='https://www.github.com/monero-ecosystem/python-monerorpc',
      download_url='https://github.com/monero-ecosystem/python-monerorpc/archive/0.5.1.tar.gz',
      packages=['monerorpc'],
      install_requires=[
          'requests',
      ],
      classifiers=['License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)', 'Operating System :: OS Independent'])
