#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from six.moves.urllib import parse


class ServiceManager(object):

    def __init__(self, client):
        """Initializes GatesManager with `client`.

        :param client: instance of BaseClient descendant for HTTP requests
        """
        super(ServiceManager, self).__init__()
        self.client = client
        
    def list(self, **kwargs):
        """Get a list of gates."""
        params = {}
        if kwargs.get('index'):
            params['index'] = kwargs['index']
        if kwargs.get('type'):
            params['type'] = kwargs['type']
        if kwargs.get('all_projects') is not None:
            params['all_projects'] = kwargs['all_projects']
        url = '/ssh_services?%s' % parse.urlencode(params, True)
        body = self.client.get(url)
        return body

