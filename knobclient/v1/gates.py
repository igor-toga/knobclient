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
            

class GatesManager(object):

    def __init__(self, client):
        """Initializes GatesManager with `client`.

        :param client: instance of BaseClient descendant for HTTP requests
        """
        super(GatesManager, self).__init__()
        self.client = client
        
    def list(self, **kwargs):
        """Get a list of gates. """
        url = '/gates?%s' % parse.urlencode(kwargs)
        body = self.client.get(url)
        return body['gates']

    def get(self, gate_name):
        """Get the details for a specific gate.

        :param gate_id: ID of the gate
        """
        body = self.client.get('/gates/%s' % gate_name)
        return body['gates']

    def create(self, **kwargs):
        """Create a gate."""
        body = self.client.post('/gates', data=kwargs)
        return body['gates']

    def delete(self, gate_name):
        """Delete a gate."""
        self.client.delete("/gates/%s" % gate_name)

    def add_target(self, gate, **kwargs):
        """Add target VM to list of allowed targets on gate"""
        body = self.client.post("/gates/%s/targets", data=kwargs)
        return body['targets']
        
    def remove_target(self, gate_name, target):
        """Delete a target from gate."""
        self.client.delete("/gates/%s/targets/%s" % (gate_name, target))
        
    def list_targets(self, gate, **kwargs):
        """Get a list of targets on gate. """
        url = '/gates/%s/targets?%s' % (gate, parse.urlencode(kwargs))
        body = self.client.get(url)
        return body['targets']
    
    def add_key(self, gate, **kwargs):
        """Add an authorized key to keys on gate"""
        body = self.client.post("/gates/%s/keys", data=kwargs)
        return body['keys']
        
    def remove_key(self, gate_name, key):
        """Delete an authorized key from gate."""
        self.client.delete("/gates/%s/keys/%s" % (gate_name, key))
        
    def list_keys(self, gate, **kwargs):
        """Get a list of authorized keys on gate. """
        url = '/gates/%s/keys?%s' % (gate, parse.urlencode(kwargs))
        body = self.client.get(url)
        return body['keys']