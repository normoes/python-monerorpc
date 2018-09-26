#!/usr/bin/env python

from distutils.core import setup

setup(name='python-monerorpc',
      version='0.1',
      description='Enhanced version of python-jsonrpc for use with Monero RPC forked from python-bitcoinrpc',
      long_description=open('README').read(),
      author='Norman Moeschter-Schenck',
      author_email='<norman.moeschter@gmail.com>',
      maintainer='Norman Moeschter-Schenck',
      maintainer_email='<norman.moeschter@gmail.com>',
      url='http://www.github.com/normoes/python-monerorpc',
      packages=['monerorpc'],
      classifiers=['License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)', 'Operating System :: OS Independent'])
