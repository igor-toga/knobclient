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

"""Knob v1 target configuration"""

import logging

from osc_lib.command import command
from osc_lib import utils

from knobclient.i18n import _ 
from knobclient import exc as exceptions


class GenerateConfig(command.Command):
    """Create a SSH config."""

    log = logging.getLogger(__name__ + '.GenerateConfig')

    def get_parser(self, prog_name):
        parser = super(GenerateConfig, self).get_parser(prog_name)
        parser.add_argument(
            'gate_id',
            metavar='<gate_id>',
            help=_('Gate id to pass trough')
        )
        parser.add_argument(
            'gate_key_file',
            metavar='<gate_key_file>',
            help=_('Gate private key file path')
        )
        parser.add_argument(
            'target_id',
            metavar='<target_id>',
            help=_('Target to connect to')
        )
        parser.add_argument(
            'user',
            metavar='<user>',
            help=_('Target username')
        )
        
        parser.add_argument(
            'target_key_file',
            metavar='<target_key_file>',
            help=_('target private key file path')
        )
        
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        knob_client = self.app.client_manager.knob

        fields = {
            'gate_id': parsed_args.gate_id,
            'gate_key_file': parsed_args.gate_key_file,
            'target_id': parsed_args.target_id,
            'user': parsed_args.user,
            'target_key_file': parsed_args.target_key_file
            }
            
        try:
            target = knob_client.targets.generate_config(**fields)
        except exceptions.HTTPNotFound:
            raise exceptions.CommandError(_('Target not found: %s')
                                   % parsed_args.target_id)
                
        return target['config']



