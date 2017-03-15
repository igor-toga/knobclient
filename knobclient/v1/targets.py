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

from knobclient.common import utils

class TargetsManager(object):

    def __init__(self, client):
        """Initializes GatesManager with `client`.

        :param client: instance of BaseClient descendant for HTTP requests
        """
        super(TargetsManager, self).__init__()
        self.client = client

    def list(self, **kwargs):
        """Get a list of targets."""
        url = '/targets?%s' % parse.urlencode(kwargs)
        body = self.client.get(url)
        return body['targets']

    def create(self, **kwargs):
        """Create a target."""
        print (kwargs)
        resp = self.client.post('/targets', data=kwargs)
        body = utils.get_response_body(resp)
        return body
    
    def delete(self, target_id):
        """Delete a target."""
        self.client.delete("/targets/%s" % target_id)

    def get(self, target_id, resolve_outputs=True):
        """Get the metadata for a specific target.

        :param stack_id: Stack ID to lookup
        :param resolve_outputs: If True, then outputs for this
               stack will be resolved
        """
        kwargs = {}
        if not resolve_outputs:
            kwargs['params'] = {"resolve_outputs": False}
        body = self.client.get('/targets/%s' % target_id, **kwargs)
        return body
        
