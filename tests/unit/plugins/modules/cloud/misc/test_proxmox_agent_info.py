# -*- coding: utf-8 -*-
# Copyright: (c) 2021, Andreas Botzner (@paginabianca) <andreas at botzner dot com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#
# Proxmox Tasks module unit tests.
# The API responses used in these tests were recorded from PVE version 6.4-8

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import pytest
import json

from ansible_collections.community.general.plugins.modules.cloud.misc import proxmox_agent_info
from ansible_collections.community.general.tests.unit.compat.mock import patch
from ansible_collections.community.general.tests.unit.plugins.modules.utils import set_module_args


def api_mocker(mocker):
    api = mocker.MagicMock()
    node = mocker.MagicMock()
    qemu = mocker.MagicMock()
    config = mocker.MagicMock()
    status = mocker.MagicMock()
    agent = mocker.MagicMock()
    api.nodes = mocker.MagicMock(return_value=node)
    node.qemu.get = mocker.MagicMock(return_value=qemu)
    qemu.status = mocker.MagicMock(return_value=status)
    qemu.config.get = mocker.MagicMock(return_value='{"agent":"1"}')
    qemu.agent = mocker.MagicMock(return_value=agent)
    status.current.get = mocker.MagicMock(return_value='running')
    agent.info.get = mocker.MagicMock(return_value=['supported_commands'])


@patch('ansible_collections.community.general.plugins.module_utils.proxmox.ProxmoxAnsible._connect')
def test_without_required_parameters(connect_mock, capfd, mocker):
    set_module_args({})
    with pytest.raises(SystemExit):
        proxmox_agent_info.main()
    out, err = capfd.readouterr()
    assert not err
    assert json.loads(out)['failed']


@patch('ansible_collections.community.general.plugins.module_utils.proxmox.ProxmoxAnsible._connect')
def test_get_agent_info(connect_mock, capfd, mocker):
    set_module_args({'api_host': 'proxmoxhost',
                     'api_user': 'root@pam',
                     'api_password': 'supersecret',
                     'node': 'node01',
                     'vmid': '100'})

    connect_mock.side_effect = api_mocker(mocker)
    proxmox_agent_info.HAS_PROXMOXER = True

    with pytest.raises(SystemExit):
        proxmox_agent_info.main()
    out, err = capfd.readouterr()
    print(out)
    assert not err
    assert json.loads(out)['changed'] is False
