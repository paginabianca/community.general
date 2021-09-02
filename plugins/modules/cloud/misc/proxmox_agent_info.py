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
name:
    description: Name of the VM.
    returned: On success.
    type: str
status:
    description: State of the VM.
    returned: On success
    type: str
    sample: running|stopped
acpi:
    description: If ACPI is enabled for the VM.
    type: bool
    returned: On success
agent:
    description: If QEMU guest agent is enabled.
    type: bool
    returned: On success
agent-info:
    description: Information gathered from QEMU guest agent.
    type:
    elements:
        fsinfo:
            description: File system information.
            type: str
            returned:
                - On success and QEMU guest agent is enable. Can be empty.
        hostname:
            description: Hostname configured on the system.
            type: str
            returned:
                - On success and QEMU guest agent is enable. Can be empty.
        memory-block-info:
            description: Memory block information.
            type: str
            returned:
                - On success and QEMU guest agent is enable. Can be empty.
        memory-blocks:
            description: Memory blocks in use by the system.
            type: str
            returned:
                - On success and QEMU guest agent is enable. Can be empty.
        osinfo:
            description: Operating System information.
            type: str
            returned:
                - On success and QEMU guest agent is enable. Can be empty.
        time:
            description: System time on the VM.
            type: str
            returned:
                - On success and QEMU guest agent is enable. Can be empty.
        timezone:
            description: Timezone configuration of the VM.
            type: str
            returned:
                - On success and QEMU guest agent is enable. Can be empty.
        users:
            description: Users configured on the VM.
            type: str
            returned:
                - On success and QEMU guest agent is enable. Can be empty.
        vcpus:
            description: Operating System information.
            type: str
            returned:
                - On success and QEMU guest agent is enable. Can be empty.
        interfaces:
            description: Network interfaces information.
            type: str
            returned:
                - On success and QEMU guest agent is enable. Can be empty.

arch:
    description: Architecture of the VM.
    type: str
    returned: On success. Can be empty.
audio:
    description: Audio interface configuration.
    type: str
    returned: On success. Can be empty.
autostart:
    description: If automatic restart after crash is enabled.
    type: bool
    returned: On success. Can be empty.
balloon:
    description: Amount of target RAM for the VM in MB.
    type: int
    returned: If ballooning is enabled.
bios:
    description: Bios running on the VM.
    type: str
    returned: On success
    choices:
        - seabios
        - ovmf
boot:
    description: Boot order of the VM.
    type: str
    returned: on success. Can be empty.
bootdisk:
    description: Specific device the VM boots from.
    type: str
    returned: on success. Can be empty.
cloud-init:
    description: Cloud-init configuration.
    type: dict
    elements:
        custom:
            description:
                - Custom files to replace the automatically generated
                  ones at start
            type: str
            returned: On success. Can be empty.
        password:
            description:
                - Password assigned to the user. This is generally not
                  recommended. Use SSH keys instead. Also note that other
                  cloud-init versions do not support hashed passwords.
            type: str
            returned: On success. Can be empty.
        type:
            description:
                - Type of the cloud-init configuration format. The default
                  depends on the configured operating system type. Proxmox uses
                  I(nocloud) for Linux and I(configdrive2) for Windows.
            type: str
            returned: On success. Can be empty.
        user:
            description:
                - User name to change ssh keys and password for instead of the
                  image's configured default user.
            type: str
            returned: On success. Can be empty.
        ipconfig:
            description: Specified IP addresses an gateways for the VM.
            type: str
            return: On success. Can be empty.
        nameserver:
            description: Specified DNS server.
            type: str
            returned: On success. Can be empty.
        searchdomain:
            description: Specified DNS search domain for VM.
            type: str
            returned: On success. Can be empty.
        sshkeys:
            description: Specified DNS server.
            type: str
            returned: On success. Can be empty.
cores:
    description: Numbers of cores per socket.
    returned: On success
    type: int
cpu:
    description: Emulated CPU type.
    returned: On success. Can be empty.
    type: str
cpulimit:
    description: Limit of CPU usage. Value I(0) indicates no CPU limit.
    returned: On success.
    type: int
cpuunits:
    description:
        - CPU weight for a VM. Argument is used in the kernel fair scheduler.
          The larger the number is, the more CPU time this VM gets. The number
          is relative to weights of all other running VMs.
    returned: On success.
    type: int
comments:
    description: Description of the VM.
    returned: On success. Can be empty.
    type: str
freeze:
    description: Freeze CPU at startup.
    returned: On success.
    type: bool
hostpci:
    description: Host PCI devices mapped to VM.
    type: list
    elements: string
    returned: On success. Can be empty.
hotplug:
    description: Selectively enabled hotplug features.
    type: str
    returned: On success. Can be empty.
    sample: network,disk,usb
hugepages:
    description: Hugepages memory configuration of the VM.
    type: str
    returned: On success. Can be empty.
    sample: '1024'
ide:
    description: IDE hard disks connected to the VM. Maximally 4.
    type: dict
    returned: On success. Can be empty.
    sample:
        ide:
            ide0: 'local:iso/somiso.iso,media=cdrom,size=56432K'
ivshmem:
    description: Inter-VM shared memory.
    type: str
    returned: On success. Can be empty.
keephugepages:
    description: Keep hugepages after VM shutdown and subsequent starts.
    returned: On success. Can be empty.
    type: bool
kvm:
    description: If KVM hardware virtualization is enabled.
    returned: On success.
    type: bool
machine:
    description: QEMU machine type.
    returned: On success.
    type: str
memory:
    description:
        - Amount of RAM available to the VM in MB. This is the maximum
          available amount if a balloon device is used.
    type: int
    returned: On success
    sample: 512
net:
    description: Specified network devices.
    type: dict
    returned: On success. Can be empty.
    sample:
        net:
            net0: 'virtio=5A:4E:E6:B7:75:59,bridge=vmbr7,firewall=1'
            net0: 'e1000=5A:4E:E6:B7:75:59,bridge=vmbr11,firewall=1'
numa:
    description: NUMA configuration if present.
    type: dict
    returned: On success. Can be empty.
onboot:
    description: VM is started during system bootup.
    type: bool
    returned: On success.
ostype:
    description: Operating system type running on the VM.
    type: str
    returned: On success.
    sample: l26
parallel:
    description: Mapped host parallel devices.
    type: dict
    returned: On success.
protection:
    description: Protection flag of the VM.
    type: bool
    returned: On success.
reboot:
    description: If VM is allowed to be rebooted.
    type: bool
    returned: On success.
rng0:
    description: Virt-IO based RNG device configuration.
    type: str
    returned: On success. Can be empty.
sata:
    description: SATA hard disks connected to the VM. Maximally 6
    type: dict
    returned: On success. Can be empty.
    sample:
        sata:
            sata0: 'images:vm-103-disk,size=32G'
scsi:
    description: SCSI hard disks connected to the VM. Maximally 31.
    type: dict
    returned: On success. Can be empty.
    sample:
        scsi:
            scsi: 'images:vm-103-disk,size=32G'
scsihw:
    description: SCSI controller model.
    type: str
    returned: On success.
    sample: lsi
serial:
    description: Serial devices connected to the VM. Maximally 4.
    type: dict
    returned: On success. Can be empty.
shares:
    description: Amount of memory shares for auto-ballooning.
    type: int
    returned: On success.
smbios1:
    description: Specified SMBIOS type 1 files.
    type: str
    returned: On success. Can be empty.
sockets:
    description: The number of CPU sockets.
    type: int
    returned: On success.
spice_enhancements:
    description: Additionally configured SPICE enhancements.
    type: str
    returned: On success. Can be empty.
startup:
    description: Startup and shutdown behavior of the VM.
    type: str
    returned: On success. Can be empty.
tablet:
    description: If the USB tablet device is enabled.
    type: bool
    returned: On success.
tags:
    description: Tags of the VM.
    type: str
    returned: On success.
template:
    description: If VM is a template or not.
    type: bool
    returned: On success.
usb:
    description: Configured USB devices. Maximally 5.
    type: dict
    returned: On success. Can be empty.
    sample:
        usb:
            usb0: 'spice,usb3=1'
vcpus:
    description: Number of hotplugged vcpus.
    type: int
    returned: On success.
vga:
    description: Configured VGA hardware.
    type: str
    returned: On success. Can be empty.
virtio:
    description: VIRTIO hard disks connected to the VM. Maximally 16.
    type: dict
    returned: On success. Can be empty.
    sample:
        virtio:
            virtio7: 'images:vm-103-disk,size=32G'
vmgenid:
    description: The VM generation ID.
    type: str
    returned: On success.
vmstatestorage:
    description: Default storage for VM state volume/files.
    type: str
    returned: On success. Can be empty.
watchdog:
    description: Virtual watchdog device connected to the VM.
    type: str
    returned: On success. Can be empty.
'''

from ansible.module_utils.basic import AnsibleModule, missing_required_lib
from ansible_collections.community.general.plugins.module_utils.proxmox import (
    proxmox_auth_argument_spec, ProxmoxAnsible, HAS_PROXMOXER, PROXMOXER_IMP_ERR)


class ProxmoxAgentInfoAnsible(ProxmoxAnsible):
    def get_agent_info(self, upid, node):
        agent_commands = self.get_commands(node)
        for task in tasks:
            if task.info['upid'] == upid:
                return [task]

    def get_tasks(self, node):
        commands = self.proxmox_api.nodes(node).qemu(vmid).agent('info')
        return [ProxmoxTask(task) for task in tasks]


class ProxmoxTask:
    def __init__(self, task):
        self.info = dict()
        for k, v in task.items():
            if k == 'status' and isinstance(v, str):
                self.info[k] = v
                if v != 'OK':
                    self.info['failed'] = True
            else:
                self.info[k] = v


def proxmox_agent_info_argument_spec():
    return dict(
        vmid=dict(type='str', aliases=['name'], required=True),
        node=dict(type='str', required=True),
    )


def main():
    module_args = proxmox_auth_argument_spec()
    task_info_args = proxmox_task_info_argument_spec()
    module_args.update(task_info_args)

    module = AnsibleModule(
        argument_spec=module_args,
        required_together=[('api_token_id', 'api_token_secret'),
                           ('api_user', 'api_password')],
        required_one_of=[('api_password', 'api_token_id')],
        supports_check_mode=True)
    result = dict(changed=False)

    if not HAS_PROXMOXER:
        module.fail_json(msg=missing_required_lib(
            'proxmoxer'), exception=PROXMOXER_IMP_ERR)
    proxmox = ProxmoxAnsible(module)
    node = module.params['node']
    vmid = module.params['vmid']
    result = {}
    state = None
    try:
        state = proxmox.proxmox_api.node(node).qemu(vmid).state().get()
    except Exception as e:
        module.fail_json(
            msg="Getting status of VM {0} failed with exception: '{1}'".format(vmid, str(e)))
    if state['status'] == 'stopped':
        module.fail_json(msg="VM {0} is not running.".format(vmid))
    agent = None
    try:
        agent = proxmox.proxmox_api.node(node).qemu(vmid).config().get()
    except Exception as e:
        module.fail_json(
            msg="Getting config of VM {0} failed with exception: '{1}'".format(vmid, str(e)))
    if 'agent' not in agent or agent['agent'] == 0:
        module.fail_json(
            msg="QEMU Guest Agent option not enabled.")
    command = None
    try:
        commands = proxmox.proxmox_api.node(node).quemu(vmid).agent('info')
    except Exception as e:
        module.fail_json(
            msg="Could not get supported QEMU guest agent commands on VM {0}".format(vmid))
    interfaces = None
    try:
        interfaces = proxmox.proxmox_api.node(node).qemu(
            vmid).agent('network-get-interfaces').get()
    except Exception as e:
        module.fail_json(
            msg="Could not get network interface configuration.")

    module.exit_json(interfaces=interfaces)


if __name__ == '__main__':
    main()
