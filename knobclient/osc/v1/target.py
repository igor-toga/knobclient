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

"""Knob v1 Facet target implementations"""

import logging

from osc_lib.command import command
from osc_lib import utils

from knobclient.i18n import _ 
from knobclient import exc as exceptions


class CreateTarget(command.ShowOne):
    """Create a SSH target."""

    log = logging.getLogger(__name__ + '.CreateTarget')

    def get_parser(self, prog_name):
        parser = super(CreateTarget, self).get_parser(prog_name)
        parser.add_argument(
            'gate_name',
            metavar='<gate_name>',
            help=_('Name of gate to connect target to')
        )
        parser.add_argument(
            'name',
            metavar='<name>',
            help=_('Host name to use as target endpoint')
        )
        
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        knob_client = self.app.client_manager.knob

        fields = {
            'name': parsed_args.name,
            'gate_name': parsed_args.gate_name,
            }
            
        try:
            target = knob_client.targets.create(**fields)
        except exceptions.HTTPNotFound:
            raise exceptions.CommandError(_('Target not found: %s')
                                   % parsed_args.name)
                
        rows = list(six.itervalues(target))
        columns = list(six.iterkeys(target))
        return columns, rows



class DeleteTarget(command.Command):
    """Delete target endpoint from service."""
    log = logging.getLogger(__name__ + ".DeleteTarget")

    def get_parser(self, prog_name):
        parser = super(DeleteTarget, self).get_parser(prog_name)
        parser.add_argument(
            'gate_id',
            metavar='<gate_id>',
            help=_('Service to disconnect this target from')
        )
        parser.add_argument(
            'targetname',
            metavar='<targetname>',
            help=_('Hostname endponit to disconnect from service')
        )
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        knob_client = self.app.client_manager.knob
        try:
            knob_client.targets.delete(parsed_args.service,
                                               parsed_args.hostname)
        except exceptions.HTTPServerError:
            raise exceptions.CommandError(_('Hostname <%(hostname)s> not found '
                                     'for service <%(service)s>')
                                   % {'hostname': parsed_args.targetname,
                                      'service': parsed_args.gate_id})



class ListTarget(command.Lister):
    """List Knob targets."""

    log = logging.getLogger(__name__ + ".ListTarget")

    def get_parser(self, prog_name):
        parser = super(ListTarget, self).get_parser(prog_name)
        parser.add_argument(
            "--all-projects",
            action='store_true',
            default=False,
            help="Request facet terms for all projects (admin only)"
        )
        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)", parsed_args)

        params = {
            "all_projects": parsed_args.all_projects
        }
        obj_list = self.app.client_manager.knob.targets.list(**params)
                
        if not obj_list:
            return [], []
        columns = obj_list[0]._get_generic_columns()
        data = (obj._get_generic_data() for obj in obj_list)
        return columns, data
