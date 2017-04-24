#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#

"""Knob v1 Facet gate implementations"""

import logging

from osc_lib.command import command
from osc_lib import utils
import six

from knobclient.i18n import _
from knobclient import exc as exceptions


class CreateGate(command.ShowOne):
    """Create a SSH gate."""

    log = logging.getLogger(__name__ + '.CreateGate')

    def get_parser(self, prog_name):
        parser = super(CreateGate, self).get_parser(prog_name)
        parser.add_argument(
            'name',
            metavar='<name>',
            help=_('Name of gate to create')
        )
        
        parser.add_argument(
            '--net-id',
            metavar='<net-id>',
            help=_('Network to build gate server on it')
        )
        
        parser.add_argument(
            '--public-net-id',
            metavar='<public-net-id>',
            help=_('Network to build gate server on it')
        )
                
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        knob_client = self.app.client_manager.knob

        fields = {
            'name': parsed_args.name,
            'net_id': parsed_args.net_id,
            'public_net_id': parsed_args.public_net_id
            }
            
        try:
            gate = knob_client.gates.create(**fields)
        except exceptions.HTTPNotFound:
            raise exceptions.CommandError(_('Gate not found: %s')
                                   % parsed_args.name)
                
        rows = list(six.itervalues(gate))
        columns = list(six.iterkeys(gate))
        return columns, rows
        


class DeleteGate(command.Command):
    """Delete gate endpoint from service."""
    log = logging.getLogger(__name__ + ".DeleteGate")

    def get_parser(self, prog_name):
        parser = super(DeleteGate, self).get_parser(prog_name)
        parser.add_argument(
            'gate_id',
            metavar='<gate_id>',
            help=_('gate to delete')
        )
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        knob_client = self.app.client_manager.knob
        try:
            knob_client.gates.delete(parsed_args.gate_id)
        except exceptions.HTTPNotFound:
            raise exceptions.CommandError(_('Gate not found: %s')
                                   % parsed_args.gate_id)



class ListGate(command.Lister):
    """List Knob gates."""

    log = logging.getLogger(__name__ + ".ListGate")

    def get_parser(self, prog_name):
        parser = super(ListGate, self).get_parser(prog_name)
        parser.add_argument(
            "--all-projects",
            action='store_true',
            default=False,
            help=_("Request facet terms for all projects (admin only)")
        )
        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)", parsed_args)
        params = {
            "all_projects": parsed_args.all_projects
        }
        gates = self.app.client_manager.knob.gates.list(**params)
        
        columns = ['id', 'name', 'server_id', 'fip_id', 'port_id', 'tenant_id']
        return (
            columns,
            (utils.get_dict_properties(s, columns) for s in gates)
        )
        

class ShowGate(command.ShowOne):
    """Show Knob details."""

    log = logging.getLogger(__name__ + ".ShowGate")

    def get_parser(self, prog_name):
        parser = super(ShowGate, self).get_parser(prog_name)
        parser.add_argument(
            'gate_id',
            metavar='<gate_id>',
            help='Gate to display (name or ID)',
        )
        
        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)", parsed_args)

        knob_client = self.app.client_manager.knob
        try:
            gate = knob_client.gates.get(parsed_args.gate_id)
        except exceptions.HTTPNotFound:
            raise exceptions.CommandError(_('Gate not found: %s')
                                   % parsed_args.gate_id)
            
        rows = list(six.itervalues(gate))
        columns = list(six.iterkeys(gate))
        return columns, rows
            

class GateAddTarget(command.Command):
    """Add target VM to SSH gate."""

    log = logging.getLogger(__name__ + '.GateAddTarget')

    def get_parser(self, prog_name):
        parser = super(GateAddTarget, self).get_parser(prog_name)
        parser.add_argument(
            'gate_id',
            metavar='<gate_id>',
            help=_('ID of gate to create')
        )
        parser.add_argument(
            'server_id',
            metavar='<server_id>',
            help=_('nova ID of target to add to gate')
        )
        
        parser.add_argument(
            'name',
            metavar='<name>',
            help=_('target to add to specified gate')
        )
        parser.add_argument(
            '--routable',
            action='store_true',
            default=True,
            help=_('Refer to state network VM target VM is connected to')
        )
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        knob_client = self.app.client_manager.knob
        
        fields = {
            'gate_id': parsed_args.gate_id,
            'server_id': parsed_args.server_id,
            'name': parsed_args.name,
            'routable': parsed_args.routable,
            }
        try:
            target = knob_client.gates.add_target(parsed_args.gate_id, 
                                                  **fields)
        except exceptions.HTTPNotFound:
            raise exceptions.CommandError(_('Gate not found: %s')
                                   % parsed_args.gate_id)
                
        print ('Target VM: %(target)s add to Gate: %(gate)s' % 
               {'target': parsed_args.server_id, 'gate': parsed_args.gate_id})
        return target['name']

            
class GateRemoveTarget(command.Command):
    """Remove target VM to SSH gate."""

    log = logging.getLogger(__name__ + '.GateRemoveTarget')

    def get_parser(self, prog_name):
        parser = super(GateRemoveTarget, self).get_parser(prog_name)
        parser.add_argument(
            'gate_id',
            metavar='<gate_id>',
            help=_('gate to delete')
        )
        parser.add_argument(
            'target_id',
            metavar='<target_id>',
            help=_('target to add to specified gate')
        )
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        knob_client = self.app.client_manager.knob
        
        try:
            knob_client.gates.remove_target(parsed_args.gate_id,
                                            parsed_args.target_id)
        except exceptions.HTTPNotFound:
            raise exceptions.CommandError(_('Gate not found: %s')
                                   % parsed_args.gate)



class GateListTargets(command.Lister):
    """List targets accessible via gate."""

    log = logging.getLogger(__name__ + ".ListTargets")

    def get_parser(self, prog_name):
        parser = super(GateListTargets, self).get_parser(prog_name)
        parser.add_argument(
            'gate_id',
            metavar='<gate_id>',
            help=_('gate to delete')
        )
        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)", parsed_args)
        params = {}
            
        targets = self.app.client_manager.knob.gates.list_targets(parsed_args.gate_id, **params)
        
        columns = ['server_id','name', 'gate_id','routable']
        return (
            columns,
            (utils.get_dict_properties(s, columns) for s in targets)
        )

class GateAddKey(command.Command):
    """Add public key to SSH gate."""

    log = logging.getLogger(__name__ + '.GateAddKey')

    def get_parser(self, prog_name):
        parser = super(GateAddKey, self).get_parser(prog_name)
        parser.add_argument(
            'gate_id',
            metavar='<gate_id>',
            help=_('gate to add public key to it')
        )
        parser.add_argument(
            'key_file',
            metavar='<key_file>',
            help=_('public key file path')
        )
        parser.add_argument(
            'name',
            metavar='<name>',
            help=_('Key name')
        )

        return parser
    
    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        knob_client = self.app.client_manager.knob
        
        try:
            key_content = open(parsed_args.key_file).read().strip()
        except:
            print ("FATAL: key file '%s' could not be opened." % parsed_args.key_file)
            return None
        
        fields = {
            'name': parsed_args.name,
            'key_content': key_content,
            }
        try:
            key = knob_client.gates.add_key(parsed_args.gate_id, **fields)
        except exceptions.HTTPNotFound:
            raise exceptions.CommandError(_('Key is not added to gate: %s')
                                   % parsed_args.gate_id)
                
        print ('Key: %(key)s add to Gate: %(gate)s' % 
               {'key': parsed_args.id, 'gate': parsed_args.gate_id})
        
        rows = list(six.itervalues(key))
        columns = list(six.iterkeys(key))
        return columns, rows

    
class GateRemoveKey(command.Command):
    """Remove public key from SSH gate."""

    log = logging.getLogger(__name__ + '.GateRemoveKey')

    def get_parser(self, prog_name):
        parser = super(GateRemoveKey, self).get_parser(prog_name)
        parser.add_argument(
            'gate_id',
            metavar='<gate_id>',
            help=_('gate to delete')
        )
        parser.add_argument(
            'key_id',
            metavar='<key_id>',
            help=_('gate to delete')
        )
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        knob_client = self.app.client_manager.knob
        try:
            knob_client.gates.remove_key(parsed_args.gate_id,
                                         parsed_args.key_id)
        except exceptions.HTTPNotFound:
            raise exceptions.CommandError(_('Key not found: %s')
                                   % parsed_args.key_id)


class GateListKeys(command.Lister):
    """List targets accessible via gate."""

    log = logging.getLogger(__name__ + ".ListKeys")

    def get_parser(self, prog_name):
        parser = super(GateListKeys, self).get_parser(prog_name)
        parser.add_argument(
            "gate_id",
            metavar='<gate_id>',
            help=_("Request facet terms for all projects (admin only)")
        )
        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)", parsed_args)
        params = {}
            
        keys = self.app.client_manager.knob.gates.list_keys(parsed_args.gate_id,**params)
        
        columns = ['id','name', 'gate_id', 'created_at']
        return (
            columns,
            (utils.get_dict_properties(s, columns) for s in keys)
        )
