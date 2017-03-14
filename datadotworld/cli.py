"""
data.world-py
Copyright 2017 data.world, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the
License.

You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
implied. See the License for the specific language governing
permissions and limitations under the License.

This product includes software developed at data.world, Inc.(http://www.data.world/).
"""
from __future__ import absolute_import

import click

from datadotworld.config import Config


@click.group()
@click.option('--profile', '-p', default='default', help='Account name')
@click.pass_context
def cli(ctx, profile):
    """Command group

    Allows user to specify configuration profile.

    Parameters
    ----------
    ctx
        Click's Context object
    profile
        Profile name
    """
    if ctx.obj is None:
        ctx.obj = {}
    ctx.obj['profile'] = profile
    pass


@click.command()
@click.option('--token', '-t', prompt='API token', help='Authentication token for API access '
                                                        '(obtained at: data.world/settings/advanced)')
@click.pass_obj
def configure(obj, token):
    """Configure profile

    Allows users to cache API tokens for one or more profiles

    Parameters
    ----------
    obj : dict
        Dictionary obtain from Click's context (Context.obj)
    token : str
        API token provided by the user
    """
    config = obj.get('config') or Config(obj['profile'])
    config.auth_token = token
    config.save()


cli.add_command(configure)
