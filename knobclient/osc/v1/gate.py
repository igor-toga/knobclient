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
            'gate',
            metavar='<gate>',
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
        
        parser.add_argument(
            '--key',
            metavar='<key>',
            #action='store_true',
            help=_('Public key required to connect to gate host')
        )
        
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        knob_client = self.app.client_manager.knob

        fields = {
            'name': parsed_args.gate,
            'net_id': parsed_args.net_id,
            'public_net_id': parsed_args.public_net_id
            }
        if parsed_args.key:
            fields['key'] = parsed_args.key
            
        
            
        try:
            gate = knob_client.gates.create(**fields)
        except exceptions.HTTPNotFound:
            raise exceptions.CommandError(_('Gate not found: %s')
                                   % parsed_args.gate)
                
        rows = list(six.itervalues(gate))
        columns = list(six.iterkeys(gate))
        return columns, rows
        


class DeleteGate(command.Command):
    """Delete gate endpoint from service."""
    log = logging.getLogger(__name__ + ".DeleteGate")

    def get_parser(self, prog_name):
        parser = super(DeleteGate, self).get_parser(prog_name)
        parser.add_argument(
            'gate',
            metavar='<gate>',
            help=_('gate to delete')
        )
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        knob_client = self.app.client_manager.knob
        try:
            knob_client.gates.delete(parsed_args.gate)
        except exceptions.HTTPNotFound:
            raise exceptions.CommandError(_('Hostname <%(hostname)s> not found '
                                     'for service <%(service)s>')
                                   % {'hostname': parsed_args.hostname,
                                      'service': parsed_args.service})



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
        
        columns = ['name', 'server_id', 'fip_id','tenant_id']
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
            'gate',
            metavar='<gate>',
            help='Gate to display (name or ID)',
        )
        
        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)", parsed_args)

        knob_client = self.app.client_manager.knob
        try:
            gate = knob_client.gates.get(parsed_args.gate)
        except exceptions.HTTPNotFound:
            raise exceptions.CommandError(_('Gate not found: %s')
                                   % parsed_args.gate)
            
        rows = list(six.itervalues(gate))
        columns = list(six.iterkeys(gate))
        return columns, rows
            


        