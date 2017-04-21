# data.world-py
# Copyright 2017 data.world, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the
# License.
#
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied. See the License for the specific language governing
# permissions and limitations under the License.
#
# This product includes software developed at
# data.world, Inc.(http://data.world/).

from __future__ import absolute_import

import click

from datadotworld.config import FileConfig


@click.group()
@click.option('--profile', '-p', default='default', help='Account name',
              metavar='<profile>')
@click.pass_context
def cli(ctx, profile):
    """dw commands support working with multiple data.world accounts

    \b
    Use a different <profile> value for each account.
    In the absence of a <profile>, 'default' will be used.
    """
    if ctx.obj is None:
        ctx.obj = {}
    ctx.obj['profile'] = profile
    pass


@click.command()
@click.option('--token', '-t',
              prompt='API token (obtained at: '
                     'https://data.world/settings/advanced)',
              help='Authentication token for API access')
@click.pass_obj
def configure(obj, token):
    """Use this command to configure API tokens
    """
    config = obj.get('config') or FileConfig(obj['profile'])
    config.auth_token = token
    config.save()


cli.add_command(configure)
