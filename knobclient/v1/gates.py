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

from knobclient.common import base
from knobclient.common import utils


class Gate(object):
    def __repr__(self):
        return "<Gate %s>" % self._info

    def create(self, **fields):
        return self.manager.create(self.identifier, **fields)

    def update(self, **fields):
        self.manager.update(self.identifier, **fields)

    def delete(self):
        return self.manager.delete(self.identifier)
            

class GatesManager(base.BaseManager):
    resource_class = Gate

    def list(self, **kwargs):
        """Get a list of gates."""
        url = '/gates?%s' % parse.urlencode(kwargs)
        return self._list(url, "gates")

    def create(self, **kwargs):
        """Create a gate."""
        headers = self.client.credentials_headers()
        resp = self.client.post('/gates',
                                data=kwargs, headers=headers)
        body = utils.get_response_body(resp)
        return body

    def update(self, gate_id, **kwargs):
        """Update a gate."""
        headers = self.client.credentials_headers()
        if kwargs.pop('existing', None):
            self.client.patch('/gates/%s' % gate_id, data=kwargs,
                              headers=headers)
        else:
            self.client.put('/gates/%s' % gate_id, data=kwargs,
                            headers=headers)

    def delete(self, gate_id):
        """Delete a gate."""
        self._delete("/gates/%s" % gate_id)

    def get(self, gate_id, resolve_outputs=True):
        """Get the metadata for a specific gate.

        :param stack_id: Stack ID to lookup
        :param resolve_outputs: If True, then outputs for this
               stack will be resolved
        """
        kwargs = {}
        if not resolve_outputs:
            kwargs['params'] = {"resolve_outputs": False}
        resp = self.client.get('/gates/%s' % gate_id, **kwargs)
        body = utils.get_response_body(resp)
        return Gate(self, body.get('gate'))
