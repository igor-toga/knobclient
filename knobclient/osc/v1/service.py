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

"""Knob v1 Facet action implementations"""

import logging

from osc_lib.command import command
from osc_lib import utils


class ListService(command.Lister):
    """List Knob services."""

    log = logging.getLogger(__name__ + ".ListService")

    def get_parser(self, prog_name):
        parser = super(ListService, self).get_parser(prog_name)
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
        params = {
            "all_projects": parsed_args.all_projects
        }
        gates = self.app.client_manager.knob.services.list(**params)
        
        return (
            columns,
            (utils.get_dict_properties(s, columns) for s in gates)
        )
        