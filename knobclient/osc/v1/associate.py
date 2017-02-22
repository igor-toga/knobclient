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

from knobclient import exc as exceptions


class CreateAssociate(command.ShowOne):
    """Create a SSH associate and attach to given target."""

    log = logging.getLogger(__name__ + '.CreateAssociate')

    def get_parser(self, prog_name):
        parser = super(CreateAssociate, self).get_parser(prog_name)
        parser.add_argument(
            'service-name',
            metavar='<service>',
            help=_('Name of service to utilize')
        )
        parser.add_argument(
            'target-name',
            metavar='<target>',
            help=_('Name of target to connect client to')
        )
        parser.add_argument(
            'hostname',
            metavar='<hostname>',
            help=_('Host name to use as target endpoint')
        )
        parser.add_argument(
            '--public-key',
            metavar='<key_id>',
            help=_('Public key required to connect to target host')
        )
        parser.add_argument(
            '--public-key-file',
            metavar='<key-file>',
            help=_('Name of public key file to load')
        )
        parser.add_argument(
            '--generate',
            metavar='<None>',
            help=_('Generate key pair to access target endpoint')
        )
        
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        knob_client = self.app.client_manager.knob

        try:
            data = knob_client.associates.create(parsed_args.service,
                                              parsed_args.hostname)
        except exceptions.HTTPNotFound:
            raise exceptions.CommandError(_('Target not found: %s')
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



class DeleteAssociate(command.Command):
    """Delete target's associate"""
    log = logging.getLogger(__name__ + ".DeleteAssociate")

    def get_parser(self, prog_name):
        parser = super(DeleteAssociate, self).get_parser(prog_name)
        parser.add_argument(
            'service-name',
            metavar='<service>',
            help=_('Service to disconnect this target from')
        )
        parser.add_argument(
            'target-name',
            metavar='<target>',
            help=_('Hostname endponit to disconnect from')
        )
        parser.add_argument(
            'hostname',
            metavar='<hostname>',
            help=_('Hostname endponit to disconnect from target')
        )
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        knob_client = self.app.client_manager.knob
        try:
            knob_client.associates.delete(parsed_args.service,
                                               parsed_args.hostname)
        except exceptions.HTTPNotFound:
            raise exceptions.CommandError(_('Hostname <%(hostname)s> not found '
                                     'to delete from target: <%(target)s>')
                                   % {'hostname': parsed_args.hostname,
                                      'target': parsed_args.target})



class ListAssociate(command.Lister):
    """List Knob associates for target."""

    log = logging.getLogger(__name__ + ".ListAssociate")

    def get_parser(self, prog_name):
        parser = super(ListAssociate, self).get_parser(prog_name)
        parser.add_argument(
            "--type",
            metavar="<resource-type>",
            help="Get targets for a particular resource type"
        )
        parser.add_argument(
            "--all-projects",
            action='store_true',
            default=False,
            help="Request facet terms for all projects (admin only)"
        )
        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)", parsed_args)

        knob_client = self.app.client_manager.search
        columns = (
            "Resource Type",
            "Type",
            "Name",
            "Options"
        )
        params = {
            "type": parsed_args.type,
            "all_projects": parsed_args.all_projects
        }
        data = knob_client.associates.list(**params)
        result = []
        for resource_type, values in data.items():
            if isinstance(values, list):
                # Cope with pre-1.0 service APIs
                associates = values
            else:
                associates = values['associates']
            for s in associates:
                options = []
                for o in s.get('options', []):
                    options.append(
                        str(o['key']) + '(' + str(o['doc_count']) + ')')
                s["options"] = ', '.join(options)
                s["resource_type"] = resource_type
                result.append(utils.get_dict_properties(s, columns))
        return (columns, result)
