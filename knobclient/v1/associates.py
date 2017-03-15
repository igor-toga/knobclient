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


class AssociatesManager(object):

    def __init__(self, client):
        """Initializes GatesManager with `client`.

        :param client: instance of BaseClient descendant for HTTP requests
        """
        super(AssociatesManager, self).__init__()
        self.client = client

    def list(self, **kwargs):
        """Get a list of associates."""
        url = '/associates?%s' % parse.urlencode(kwargs)
        body = self.client.get(url)
        return body

    def create(self, **kwargs):
        """Create a associate."""
        print (kwargs)
        resp = self.client.post('/associates', data=kwargs)
        body = utils.get_response_body(resp)
        return body
    
    def delete(self, associate_id):
        """Delete a associate."""
        self.client.delete("/associates/%s" % associate_id)

    def get(self, associate_id, resolve_outputs=True):
        """Get the metadata for a specific associate.

        :param stack_id: Stack ID to lookup
        :param resolve_outputs: If True, then outputs for this
               stack will be resolved
        """
        kwargs = {}
        if not resolve_outputs:
            kwargs['params'] = {"resolve_outputs": False}
        body = self.client.get('/associates/%s' % associate_id, **kwargs)
        return body
        