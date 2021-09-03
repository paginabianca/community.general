#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Andreas Botzner (@paginabianca) <andreas at botzner dot com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = r'''
---
module: proxmox_agent_info
short_description: Retrieve QEMU guest agent info about VMs on Proxmox.
version_added: 3.6.0
description:
  - Retrieve detailed information about VMs running on Proxmox that support
    the QEMU guest agent and have the service enabled.
author: 'Andreas Botzner (@paginabianca) <andreas at botzner dot com>'
options:
  node:
    description:
      - Node where VM is located.
    required: true
    type: str
  vmid:
    description:
      - VMID of the VM.
    aliases: ['name']
    required: true
    type: str
extends_documentation_fragment:
    - community.general.proxmox.documentation
'''


EXAMPLES = '''
- name: Retrieve info about VM 101 on node01
  community.general.proxmox_kvm_info:
    api_host: proxmoxhost
    api_user: root@pam
    api_password: '{{ password | default(omit) }}'
    api_token_id: '{{ token_id | default(omit) }}'
    api_token_secret: '{{ token_secret | default(omit) }}'
    node: node01
    name: 101
  register: result
'''


RETURN = '''

vmid:
    description: VMID of the VM.
    returned: On success.
    type: int
    sample: 102
msg:
    description: Short message.
    type: str
    returned: always
fsinfo:
    description: File system information.
    type: list
    elements: dict
    returned: On success. Can be empty.
    sample:
        - disk:
          - bus: 0
            bus-type: scsi
            dev: /dev/sda1
            pci-controller:
              bus: 0
              domain: 0
              function: 0
              slot: 5
            serial: 0QEMU_QEMU_HARDDISK_drive-scsi0
            target: 0
            unit: 0
          mountpoint: /boot
          name: sda1
          total-bytes: 703578112
          type: ext4
          used-bytes: 117227520
hostname:
    description: Hostname configured on the system.
    type: str
    returned: On success. Can be empty.
    sample:
memory-block-size:
    description: Memory block information.
    type: int
    returned: On success. Can be empty.
    sample: 134217728
memory-blocks:
    description: Memory blocks in use by the system.
    type: list
    elements: dict
    returned: On success. Can be empty.
    sample:
        - can-offline: true
          online: true
          phys-index: 32
        - can-offline: true
          online: true
          phys-index: 60
osinfo:
    description: Operating System information.
    type: dict
    returned: On success. Can be empty.
    sample:
        id: elementary
        kernel-release: 5.11.0-27-generic
        kernel-version: '#29~20.04.1-Ubuntu SMP Wed Aug 11 15:58:17 UTC 2021'
        machine: x86_64
        name: elementary OS
        pretty-name: elementary OS 6 Odin
        version: 6 Odin
        version-id: '6'
time:
    description: System time of the VM in UNIX time stamp format.
    type: int
    returned: On success. Can be empty.
    sample: 1630651616789051000
timezone:
    description: Timezone configuration of the VM.
    type: dict
    returned: On success. Can be empty.
    sample:
        offset: 0
        zone: UTC
users:
    description: Users configured on the VM.
    type: list
    elements: dict
    returned: On success. Can be empty.
    sample:
        - login-time: 1630593332.90773
          user: asdf
vcpus:
    description: Operating System information.
    type: list
    elements: dict
    returned: On success. Can be empty.
    sample:
        - can-offline: false
          logical-id: 0
          online: true
        - can-offline: true
          logical-id: 1
          online: true
interfaces:
    description: Network interfaces information.
    type: list
    elements: dict
    returned: On success. Can be empty.
    sample:
        - hardware-address: 00:00:00:00:00:00
          ip-addresses:
          - ip-address: 127.0.0.1
            ip-address-type: ipv4
            prefix: 8
          - ip-address: ::1
            ip-address-type: ipv6
            prefix: 128
          name: lo
          statistics:
            rx-bytes: 293399
            rx-dropped: 0
            rx-errs: 0
            rx-packets: 3791
            tx-bytes: 293399
            tx-dropped: 0
            tx-errs: 0
            tx-packets: 3791
        - hardware-address: 42:7a:2a:fc:16:0f
          ip-addresses:
          - ip-address: 10.0.10.12
            ip-address-type: ipv4
            prefix: 23
          - ip-address: fe80::6ccc:4711:184c:8aaa
            ip-address-type: ipv6
            prefix: 64
          name: ens18
          statistics:
            rx-bytes: 10494087
            rx-dropped: 0
            rx-errs: 0
            rx-packets: 40701
            tx-bytes: 620415
            tx-dropped: 0
            tx-errs: 0
            tx-packets: 6213
'''

from ansible.module_utils.basic import AnsibleModule, missing_required_lib
from ansible_collections.community.general.plugins.module_utils.proxmox import (
    proxmox_auth_argument_spec, ProxmoxAnsible, HAS_PROXMOXER, PROXMOXER_IMP_ERR)

QEMU_GET_COMMANDS = {
    'get-fsinfo': 'fsinfo',
    'get-host-name': 'hostname',
    'get-memory-block-info': 'memory-block-size',
    'get-memory-blocks': 'memory-blocks',
    'get-osinfo': 'osinfo',
    'get-time': 'time',
    'get-timezone': 'timezone',
    'get-users': 'users',
    'get-vcpus': 'vcpus',
    'network-get-interfaces': 'interfaces'}


def proxmox_agent_info_argument_spec():
    return dict(
        vmid=dict(type='str', aliases=['name'], required=True),
        node=dict(type='str', required=True),
    )


def main():
    module_args = proxmox_auth_argument_spec()
    task_info_args = proxmox_agent_info_argument_spec()
    module_args.update(task_info_args)

    module = AnsibleModule(
        argument_spec=module_args,
        required_together=[('api_token_id', 'api_token_secret'),
                           ('api_user', 'api_password')],
        required_one_of=[('api_password', 'api_token_id')],
        supports_check_mode=True)

    if not HAS_PROXMOXER:
        module.fail_json(msg=missing_required_lib(
            'proxmoxer'), exception=PROXMOXER_IMP_ERR)
    proxmox = ProxmoxAnsible(module)
    node = module.params['node']
    vmid = module.params['vmid']
    result = {'vmid': vmid, 'changed': False}
    state = None
    try:
        state = proxmox.proxmox_api.nodes(
            node).qemu(vmid).status('current').get()
    except Exception as e:
        module.fail_json(
            msg="Getting status of VM {0} failed with exception: '{1}'".format(vmid, str(e)))
    if state['status'] == 'stopped':
        module.fail_json(msg="VM {0} is not running.".format(vmid))
    agent = None
    try:
        agent = proxmox.proxmox_api.nodes(node).qemu(vmid).config().get()
    except Exception as e:
        module.fail_json(
            msg="Getting config of VM {0} failed with exception: '{1}'".format(vmid, str(e)))
    if 'agent' not in agent or agent['agent'] == 0:
        module.fail_json(
            msg="QEMU Guest Agent option not enabled.")
    qemu_commands = {}
    try:
        cmd = proxmox.proxmox_api.nodes(
            node).qemu(vmid).agent('info').get()
        for command in cmd['result']['supported_commands']:
            qemu_commands[command.pop('name')] = command
    except Exception as e:
        module.fail_json(
            msg="Failed getting supported QEMU guest agent commands with error: {0}".format(str(e)))

    for k, v in QEMU_GET_COMMANDS.items():
        if 'guest-' + k not in qemu_commands:
            continue
        if not qemu_commands['guest-' + k]['enabled']:
            continue
        if not qemu_commands['guest-' + k]['success-response']:
            continue
        try:
            res = proxmox.proxmox_api.nodes(
                node).qemu(vmid).agent(k).get()
            if k == 'hostname':
                result[v] = res['host-name']
                continue
            if k == 'memory-block-info':
                result[v] = res['size']
                continue
            result[v] = res
        except Exception as e:
            module.fail_json(
                msg="Failed to execute {0} with error: {1}".format(k, str(e)))

    module.exit_json(**result)


if __name__ == '__main__':
    main()
