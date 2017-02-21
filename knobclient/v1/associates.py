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


class Associate(base.Resource):
    def __repr__(self):
        return "<Associate %s>" % self._info

    def create(self, **fields):
        return self.manager.create(self.identifier, **fields)

    def update(self, **fields):
        self.manager.update(self.identifier, **fields)

    def delete(self):
        return self.manager.delete(self.identifier)

    def get(self):
        # set_loaded() first ... so if we have to bail, we know we tried.
        self._loaded = True
        if not hasattr(self.manager, 'get'):
            return

        new = self.manager.get(self.identifier)
        if new:
            self._add_details(new._info)

class AssociatesManager(base.BaseManager):
    resource_class = Associate

    def list(self, **kwargs):
        """Get a list of associates."""

    def create(self, **kwargs):
        """Create an associate."""
        headers = self.client.credentials_headers()
        resp = self.client.post('/associates',
                                data=kwargs, headers=headers)
        body = utils.get_response_body(resp)
        return body

    def update(self, associate_id, **kwargs):
        """Update an associate."""
        headers = self.client.credentials_headers()
        if kwargs.pop('existing', None):
            self.client.patch('/associates/%s' % associate_id, data=kwargs,
                              headers=headers)
        else:
            self.client.put('/associates/%s' % associate_id, data=kwargs,
                            headers=headers)

    def delete(self, associate_id):
        """Delete an associate."""
        self._delete("/associates/%s" % associate_id)

    def get(self, stack_id, resolve_outputs=True):
        """Get the metadata for a specific associate.

        :param stack_id: Stack ID to lookup
        :param resolve_outputs: If True, then outputs for this
               stack will be resolved
        """
        kwargs = {}
        if not resolve_outputs:
            kwargs['params'] = {"resolve_outputs": False}
        resp = self.client.get('/associates/%s' % stack_id, **kwargs)
        body = utils.get_response_body(resp)
        return Associate(self, body.get('associate'))
