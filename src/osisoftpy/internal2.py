# -*- coding: utf-8 -*-

#    Copyright 2017 DST Controls
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
"""
osisoftpy.internal
~~~~~~~~~~~~
Some blah blah about what this file is for...
"""

import logging

import requests
import requests_kerberos
import wrapt
from collections import namedtuple
from osisoftpy.exceptions import PIWebAPIError

log = logging.getLogger(__name__)


@wrapt.decorator
def wrapt_handle_exceptions(wrapped, instance, args, kwargs):
    try:
        return wrapped(*args, **kwargs)
    except PIWebAPIError as e:
        log.debug(e, exc_info=False)
        raise e
    except Exception as e:
        log.debug(e, exc_info=True)
        raise e


@wrapt_handle_exceptions
def get(url, session=None, params=None, password=None, username=None,
    authtype=None, verifyssl=True):
    s = session or requests.session()
    with s:
        s.verify = verifyssl
        s.auth = s.auth or _get_auth(authtype, username, password)
        Response = namedtuple('Response', ['response', 'session'])
        r = Response(s.get(url, params=params), s)
        json = r.response.json()
        if 'Errors' in json and json.get('Errors').__len__() > 0:
            msg = 'PI Web API returned an error: {}'
            raise PIWebAPIError(msg.format(json.get('Errors')))
        else:
            return r


@wrapt_handle_exceptions
def put(url, session=None, params=None, password=None, username=None,
        authtype=None, verifyssl=True, **kwargs):
    s = session or requests.session()
    with s:
        s.verify = verifyssl
        s.auth = s.auth or _get_auth(authtype, username, password)
        Response = namedtuple('Response', ['response', 'session'])
        r = Response(s.put(url, params=params), s)
        json = r.response.json()
        if 'Errors' in json and json.get('Errors').__len__() > 0:
            msg = 'PI Web API returned an error: {}'
            raise PIWebAPIError(msg.format(json.get('Errors')))
        else:
            return r


@wrapt_handle_exceptions
def get_bulk(points, action, params=None, webapi=None,
         password=None, username=None, authtype=None, verifyssl=True, **kwargs):
    s = webapi.session or requests.session()
    with s:
        s.verify = verifyssl
        s.auth = s.auth or _get_auth(authtype, username, password)
        payload = {}
        url = '{}/streams/{}'.format(webapi.links.get('Self'), action)
        for p in points:
            request = s.prepare_request(requests.Request(
                'GET', '{}/{}/value'.format(url, p.webid), params=params))

            payload[p.name] = {
                'Method': request.method,
                'Resource': request.url,
            }
        Response = namedtuple('Response', ['response', 'session'])
        r = Response(s.post(url, json=payload), s)
        json = r.response.json()
        if 'Errors' in json and json.get('Errors').__len__() > 0:
            msg = 'PI Web API returned an error: {}'
            raise PIWebAPIError(msg.format(json.get('Errors')))
        else:
            return r

def _stringify(**kwargs):
    """
    Return a concatenated string of the keys and values of the kwargs
    Source: http://stackoverflow.com/a/39623935
    :param kwargs: kwargs to be combined into a single string
    :return: String representation of the kwargs
    """
    return (','.join('{0}={1!r}'.format(k, v)
                     for k, v in kwargs.items()))


def _get_auth(authtype, username=None, password=None):
    if authtype == 'kerberos':
        return requests_kerberos.HTTPKerberosAuth(
            mutual_authentication=requests_kerberos.OPTIONAL)
    else:
        return requests.auth.HTTPBasicAuth(username, password)