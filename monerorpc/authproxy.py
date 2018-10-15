
"""
  Copyright 2011 Jeff Garzik

  Forked by Norman Schenck from python-bitcoinrpc in 09/2018.
  python-monerorpc is based on this fork.


  AuthServiceProxy has the following improvements over python-jsonrpc's
  ServiceProxy class:

  - HTTP connections persist for the life of the AuthServiceProxy object
    (if server supports HTTP/1.1)
  - sends protocol 'jsonrpc', per JSON-RPC 2.0
  - sends proper, incrementing 'id'
  - sends Digest HTTP authentication headers
  - parses all JSON numbers that look like floats as Decimal
  - uses standard Python json lib

  Previous copyright, from python-jsonrpc/jsonrpc/proxy.py:

  Copyright (c) 2007 Jan-Klaas Kollhof

  This file is part of jsonrpc.

  jsonrpc is free software; you can redistribute it and/or modify
  it under the terms of the GNU Lesser General Public License as published by
  the Free Software Foundation; either version 2.1 of the License, or
  (at your option) any later version.

  This software is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU Lesser General Public License for more details.

  You should have received a copy of the GNU Lesser General Public License
  along with this software; if not, write to the Free Software
  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
"""

from requests import auth, Session, codes
import decimal
import json
import logging
try:
    import urllib.parse as urlparse
except ImportError:
    import urlparse

USER_AGENT = "AuthServiceProxy/0.1"

HTTP_TIMEOUT = 30

log = logging.getLogger("MoneroRPC")


class JSONRPCException(Exception):
    def __init__(self, rpc_error):
        parent_args = []
        try:
            parent_args.append(rpc_error['message'])
        except Exception:
            pass
        Exception.__init__(self, *parent_args)
        self.error = rpc_error
        self.code = rpc_error['code'] if 'code' in rpc_error else None
        self.message = rpc_error['message'] if 'message' in rpc_error else None

    def __str__(self):
        return '%d: %s' % (self.code, self.message)

    def __repr__(self):
        return '<%s \'%s\'>' % (self.__class__.__name__, self)


def EncodeDecimal(o):
    if isinstance(o, decimal.Decimal):
        return float(round(o, 12))
    raise TypeError(repr(o) + " is not JSON serializable")


class AuthServiceProxy(object):
    """Extension of python-jsonrpc
    to communicate with Monero (monerod, monero-walletrpc)
    """
    __id_count = 0

    def __init__(self, service_url, service_name=None, timeout=HTTP_TIMEOUT,
                 connection=None):
        """
        :param service_url: http://user:passwd@host:port/json_rpc"
        :param service_name: method name of monero wallet RPC and monero daemon RPC
        """
        self.__service_url = service_url
        self.__service_name = service_name
        self.__timeout = timeout
        self.__url = urlparse.urlparse(service_url)
        if self.__url.port is None:
            port = 80
        else:
            port = self.__url.port

        self.__rpc_url = (self.__url.scheme
                          + '://' + self.__url.hostname
                          + ':' + str(port)
                          + self.__url.path)

        (user, passwd) = (self.__url.username, self.__url.password)

        # Digest Authentication
        authentication = None
        log.debug('{0}, {1}'.format(user, passwd))
        if user is not None and passwd is not None:
            authentication = auth.HTTPDigestAuth(user, passwd)

        headers = {'Content-Type': 'application/json',
                   'User-Agent': USER_AGENT,
                   'Host': self.__url.hostname}

        if connection:
            # Callables re-use the connection of the original proxy
            self.__conn = connection
        else:
            self.__conn = Session()
            self.__conn.auth = authentication
            self.__conn.headers = headers

    def __getattr__(self, name):
        if name.startswith('__') and name.endswith('__'):
            # Python internal stuff
            raise AttributeError
        if self.__service_name is not None:
            name = '{0}.{1}'.format(self.__service_name, name)
        return AuthServiceProxy(self.__service_url, name,
                                connection=self.__conn)

    def __call__(self, *args):
        AuthServiceProxy.__id_count += 1

        log.debug('-{0}-> {1} {2}'.format(AuthServiceProxy.__id_count,
                                          self.__service_name,
                                          json.dumps(args,
                                                     default=EncodeDecimal)))
        # args is tuple
        # monero RPC always gets one dictionary as parameter
        if args:
            args = args[0]

        postdata = json.dumps({'jsonrpc': '2.0',
                               'method': self.__service_name,
                               'params': args,
                               'id': AuthServiceProxy.__id_count},
                              default=EncodeDecimal)
        return self._request(postdata)

    def batch_(self, rpc_calls):
        """Batch RPC call.
           Pass array of arrays: [ [ "method", params... ], ... ]
           Returns array of results.

           No real implementation of JSON RPC batch.
           Only requesting every method one after another.
        """
        results = list()
        for rpc_call in rpc_calls:
            method = rpc_call.pop(0)
            params = rpc_call.pop(0) if rpc_call else dict()
            results.append(self.__getattr__(method)(params))

        return results

    def _request(self, postdata):
        log.debug('--> {}'.format(postdata))
        r = self.__conn.post(url=self.__rpc_url,
                             data=postdata,
                             timeout=self.__timeout)

        response = self._get_response(r)
        if response.get('error', None) is not None:
            raise JSONRPCException(response['error'])
        elif 'result' not in response:
            raise JSONRPCException({
                'code': -343, 'message': 'missing JSON-RPC result'})
        else:
            return response['result']

    def _get_response(self, r):
        if r.status_code != codes.ok:
            raise JSONRPCException({'code': -344,
                                   'message': 'received HTTP status code {}'.format(r.status_code)})
        http_response = r.text
        if http_response is None:
            raise JSONRPCException({
                'code': -342, 'message': 'missing HTTP response from server'})

        response = json.loads(http_response,
                              parse_float=decimal.Decimal)
        if 'error' in response and response.get('error', None) is None:
            log.error('error: {}'.format(response))
            log.debug('<-{0}- {1}'.format(response['id'],
                                          json.dumps(response['result'],
                                                     default=EncodeDecimal)))
        else:
            log.debug('<-- {}'.format(response))
        return response
