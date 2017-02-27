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

"""OpenStackClient plugin for Knob service."""

from osc_lib import utils

DEFAULT_KNOB_API_VERSION = '1'
API_VERSION_OPTION = 'os_knob_api_version'
API_NAME = 'knob'
API_VERSIONS = {
    '1': 'knobclient.client.Client',
}


def make_client(instance):
    """Returns a knob service client"""
    knob_client = utils.get_client_class(
        API_NAME,
        instance._api_version[API_NAME],
        API_VERSIONS)

    # Remember interface only if it is set
    kwargs = utils.build_kwargs_dict('endpoint_type', instance._interface)
    client = knob_client(
        session=instance.session,
        region_name=instance._region_name,
        **kwargs
    )

    return client


def build_option_parser(parser):
    """Hook to add global options"""
    parser.add_argument(
        '--os-knob-api-version',
        metavar='<knob-api-version>',
        default=utils.env(
            'OS_KNOB_API_VERSION',
            default=DEFAULT_KNOB_API_VERSION),
        help='Knob API version, default=' +
             DEFAULT_KNOB_API_VERSION +
             ' (Env: OS_KNOB_API_VERSION)')
    return parser
