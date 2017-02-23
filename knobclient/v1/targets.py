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
import six
from six.moves.urllib import parse

from knobclient.i18n import _
from knobclient.common import base
from knobclient.common import utils
from knobclient import exc


class Target(base.Resource):
    def __repr__(self):
        return "<Target %s>" % self._info

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
            

class TargetsManager(base.BaseManager):
    resource_class = Target

    def list(self, **kwargs):
        """Get a list of targets."""

    def create(self, **kwargs):
        """Create a target."""
        headers = self.client.credentials_headers()
        resp = self.client.post('/targets',
                                data=kwargs, headers=headers)
        body = utils.get_response_body(resp)
        return body

    def update(self, target_id, **kwargs):
        """Update a target."""
        headers = self.client.credentials_headers()
        if kwargs.pop('existing', None):
            self.client.patch('/targets/%s' % target_id, data=kwargs,
                              headers=headers)
        else:
            self.client.put('/targets/%s' % target_id, data=kwargs,
                            headers=headers)

    def delete(self, target_id):
        """Delete a target."""
        self._delete("/targets/%s" % target_id)

    def get(self, stack_id, resolve_outputs=True):
        """Get the metadata for a specific target.

        :param stack_id: Stack ID to lookup
        :param resolve_outputs: If True, then outputs for this
               stack will be resolved
        """
        kwargs = {}
        if not resolve_outputs:
            kwargs['params'] = {"resolve_outputs": False}
        resp = self.client.get('/targets/%s' % stack_id, **kwargs)
        body = utils.get_response_body(resp)
        return Target(self, body.get('target'))