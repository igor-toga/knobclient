# Copyright (c) 2013 Rackspace, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import os

from keystoneauth1 import adapter
from keystoneauth1 import session as ks_session
from oslo_serialization import jsonutils

from knobclient.v1 import targets
from knobclient.v1 import gates
from knobclient.v1 import services
from knobclient import exc as exceptions


LOG = logging.getLogger(__name__)
_DEFAULT_SERVICE_TYPE = 'ssh'
_DEFAULT_SERVICE_INTERFACE = 'public'
_DEFAULT_API_VERSION = 'v1'


class _HTTPClient(adapter.Adapter):

    def __init__(self, session, project_id=None, **kwargs):
        kwargs.setdefault('interface', _DEFAULT_SERVICE_INTERFACE)
        kwargs.setdefault('service_type', _DEFAULT_SERVICE_TYPE)
        kwargs.setdefault('version', _DEFAULT_API_VERSION)
        endpoint = kwargs.pop('endpoint', None)

        super(_HTTPClient, self).__init__(session, **kwargs)

        if endpoint:
            self.endpoint_override = '{0}/{1}'.format(endpoint, self.version)

        if project_id is None:
            self._default_headers = dict()
        else:
            # If provided we'll include the project ID in all requests.
            self._default_headers = {'X-Project-Id': project_id}

    def request(self, *args, **kwargs):
        headers = kwargs.setdefault('headers', {})
        headers.update(self._default_headers)

        # Set raise_exc=False by default so that we handle request exceptions
        kwargs.setdefault('raise_exc', False)
        
        resp = super(_HTTPClient, self).request(*args, **kwargs)
        self._check_status_code(resp)
        return resp

    def get(self, *args, **kwargs):
        headers = kwargs.setdefault('headers', {})
        headers.setdefault('Content-Type', 'application/json')
        headers.setdefault('Accept', 'application/json')
        headers.setdefault('X-Project-Name', os.environ['OS_PROJECT_NAME'])
        headers.setdefault('X-User-Name', os.environ['OS_USERNAME'])
        headers.setdefault('X-User-Domain-Id', os.environ['OS_USER_DOMAIN_ID'])
        headers.setdefault('X-Project-Domain-Id', os.environ['OS_PROJECT_DOMAIN_ID'])

        return super(_HTTPClient, self).get(*args, **kwargs).json()

    def post(self, *args, **kwargs):
        #path = self._fix_path(path)
        headers = kwargs.setdefault('headers', {})
        headers.setdefault('Content-Type', 'application/json')
        headers.setdefault('Accept', 'application/json')
        headers.setdefault('X-Project-Name', os.environ['OS_PROJECT_NAME'])
        headers.setdefault('X-User-Name', os.environ['OS_USERNAME'])
        headers.setdefault('X-User-Domain-Id', os.environ['OS_USER_DOMAIN_ID'])
        headers.setdefault('X-Project-Domain-Id', os.environ['OS_PROJECT_DOMAIN_ID'])


        if 'data' in kwargs:
            kwargs['data'] = jsonutils.dumps(kwargs['data'])

        return super(_HTTPClient, self).post(*args, **kwargs).json()

    def delete(self, *args, **kwargs):
        headers = kwargs.setdefault('headers', {})
        headers.setdefault('Content-Type', 'application/octet-stream')
        headers.setdefault('X-Project-Name', os.environ['OS_PROJECT_NAME'])
        headers.setdefault('X-User-Name', os.environ['OS_USERNAME'])
        headers.setdefault('X-User-Domain-Id', os.environ['OS_USER_DOMAIN_ID'])
        headers.setdefault('X-Project-Domain-Id', os.environ['OS_PROJECT_DOMAIN_ID'])

        
        return super(_HTTPClient, self).delete(*args, **kwargs).json()
        
    def _fix_path(self, path):
        if not path[-1] == '/':
            path += '/'
        return path

    def _get_raw(self, path, *args, **kwargs):
        return self.request(path, 'GET', *args, **kwargs).content

    def _check_status_code(self, resp):
        status = resp.status_code
        LOG.debug('Response status {0}'.format(status))
        if status == 401:
            LOG.error('Auth error: {0}'.format(self._get_error_message(resp)))
            raise exceptions.HTTPAuthError(
                '{0}'.format(self._get_error_message(resp))
            )
        if not status or status >= 500:
            LOG.error('5xx Server error: {0}'.format(
                self._get_error_message(resp)
            ))
            raise exceptions.HTTPServerError(
                '{0}'.format(self._get_error_message(resp)),
                status
            )
        if status >= 400:
            LOG.error('4xx Client error: {0}'.format(
                self._get_error_message(resp)
            ))
            raise exceptions.HTTPClientError(
                '{0}'.format(self._get_error_message(resp)),
                status
            )

    def _get_error_message(self, resp):
        try:
            response_data = resp.json()
            message = response_data['title']
            description = response_data.get('description')
            if description:
                message = '{0}: {1}'.format(message, description)
        except ValueError:
            message = resp.content
        return message


class Client(object):

    def __init__(self, session=None, *args, **kwargs):
        """
        Knob client object used to interact with knob service.

        :param session: An instance of keystoneclient.session.Session that
            can be either authenticated, or not authenticated.  When using
            a non-authenticated Session, you must provide some additional
            parameters.  When no session is provided it will default to a
            non-authenticated Session.
        :param endpoint: Knob endpoint url. Required when a session is not
            given, or when using a non-authenticated session.
            When using an authenticated session, the client will attempt
            to get an endpoint from the session.
        :param project_id: The project ID used for context in Knob.
            Required when a session is not given, or when using a
            non-authenticated session.
            When using an authenticated session, the project ID will be
            provided by the authentication mechanism.
        :param verify: When a session is not given, the client will create
            a non-authenticated session.  This parameter is passed to the
            session that is created.  If set to False, it allows
            knobclient to perform "insecure" TLS (https) requests.
            The server's certificate will not be verified against any
            certificate authorities.
            WARNING: This option should be used with caution.
        :param service_type: Used as an endpoint filter when using an
            authenticated keystone session. Defaults to 'key-management'.
        :param service_name: Used as an endpoint filter when using an
            authenticated keystone session.
        :param interface: Used as an endpoint filter when using an
            authenticated keystone session. Defaults to 'public'.
        :param region_name: Used as an endpoint filter when using an
            authenticated keystone session.
        """
        LOG.debug("Creating Client object")

        if not session:
            session = ks_session.Session(verify=kwargs.pop('verify', True))

        if session.auth is None and kwargs.get('auth') is None:
            if not kwargs.get('endpoint'):
                raise ValueError('Knob endpoint url must be provided when '
                                 'not using auth in the Keystone Session.')

            if kwargs.get('project_id') is None:
                raise ValueError('Project ID must be provided when not using '
                                 'auth in the Keystone Session')

        httpclient = _HTTPClient(session=session, *args, **kwargs)

        self.gates = gates.GatesManager(httpclient)
        self.targets = targets.TargetsManager(httpclient)
        self.services = services.ServiceManager(httpclient)
        