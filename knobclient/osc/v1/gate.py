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

from knobclient import exc as exceptions


class CreateGate(command.ShowOne):
    """Create a SSH gate."""

    log = logging.getLogger(__name__ + '.CreateGate')

    def get_parser(self, prog_name):
        parser = super(CreateGate, self).get_parser(prog_name)
        parser.add_argument(
            'service-name',
            metavar='<service>',
            help=_('Name of service to connect gate to')
        )
        parser.add_argument(
            'hostname',
            metavar='<hostname>',
            help=_('Host name to use as gate endpoint')
        )
        parser.add_argument(
            '--public-key',
            metavar='<key_id>',
            help=_('Public key required to connect to gate host')
        )
        parser.add_argument(
            '--public-key-file',
            metavar='<key-file>',
            help=_('Name of public key file to load')
        )
        parser.add_argument(
            '--generate',
            metavar='<None>',
            help=_('Generate key pair to access gate endpoint')
        )
        
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        knob_client = self.app.client_manager.knob

        try:
            data = knob_client.gates.create(parsed_args.service,
                                              parsed_args.hostname)
        except exceptions.HTTPNotFound:
            raise exceptions.CommandError(_('Gate not found: %s')
                                   % parsed_args.stack)

        columns = [
            'ID',
            'name',
            'status',
            'status_reason',
            'data',
            'creation_time'
        ]
        return (columns, utils.get_dict_properties(data, columns))



class DeleteGate(command.Command):
    """Delete gate endpoint from service."""
    log = logging.getLogger(__name__ + ".DeleteGate")

    def get_parser(self, prog_name):
        parser = super(DeleteGate, self).get_parser(prog_name)
        parser.add_argument(
            'service-name',
            metavar='<service>',
            help=_('Service to disconnect this gate from')
        )
        parser.add_argument(
            'hostname',
            metavar='<hostname>',
            help=_('Hostname endponit to disconnect from service')
        )
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        knob_client = self.app.client_manager.knob
        try:
            knob_client.gates.delete(parsed_args.service,
                                               parsed_args.hostname)
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
            help="Request facet terms for all projects (admin only)"
        )
        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)", parsed_args)
        columns = ['tenant_id', 'name', 'project_id','status']
        #params = {
        #    "all_projects": parsed_args.all_projects
        #}
        params = {}
        gates = self.app.client_manager.knob.gates.list(**params)
        
        return (
            columns,
            (utils.get_dict_properties(s, columns) for s in gates)
        )
