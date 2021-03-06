# flink

[![Build Status](https://img.shields.io/travis/Temelio/ansible-role-flink/master.svg?label=travis_master)](https://travis-ci.org/Temelio/ansible-role-flink)
[![Build Status](https://img.shields.io/travis/Temelio/ansible-role-flink/develop.svg?label=travis_develop)](https://travis-ci.org/Temelio/ansible-role-flink)
[![Updates](https://pyup.io/repos/github/Temelio/ansible-role-flink/shield.svg)](https://pyup.io/repos/github/Temelio/ansible-role-flink/)
[![Python 3](https://pyup.io/repos/github/Temelio/ansible-role-flink/python-3-shield.svg)](https://pyup.io/repos/github/Temelio/ansible-role-flink/)
[![Ansible Role](https://img.shields.io/ansible/role/19271.svg)](https://galaxy.ansible.com/Temelio/flink/)

Install flink package.

## Requirements

This role requires Ansible 2.2 or higher,
and platform requirements are listed in the metadata file.

This role need a java installation, but no dependency defined, you can use the role you want (ex: infOpen.openjdk_jre)

## Testing

This role use [Molecule](https://github.com/metacloud/molecule/) to run tests.

Local and Travis tests run tests on Docker by default.
See molecule documentation to use other backend.

Currently, tests are done on:
- Debian Jessie
- Ubuntu Trusty
- Ubuntu Xenial

and use:
- Ansible 2.2.x
- Ansible 2.3.x
- Ansible 2.4.x

### Running tests

#### Using Docker driver

```
$ tox
```

## Role Variables

### Default role variables

``` yaml
# Installation variables
#------------------------------------------------------------------------------

# Package variables
flink_version: '1.3.1'
flink_package: "flink-{{ flink_version }}"
flink_package_filename: "{{ flink_package }}-bin-hadoop2-scala_2.10.tgz"
flink_download_url: "http://archive.apache.org/dist/flink/flink-{{ flink_version }}/{{ flink_package_filename }}"
flink_system_dependencies: "{{ _flink_system_dependencies }}"

# Installation folder
flink_root_dir:
  path: "{{ flink_user.home | default('/var/lib/flink') }}"
  user: "{{ flink_user.name }}"
  group: "{{ flink_group.name }}"
  mode: '0750'

# Log folder
flink_log_dir:
  path: '/var/log/flink'
  user: "{{ flink_user.name }}"
  group: "{{ flink_group.name }}"
  mode: '0750'

# PID folder
flink_pid_dir:
  path: '/var/run/flink'
  user: "{{ flink_user.name }}"
  group: "{{ flink_group.name }}"
  mode: '0750'

# User management
flink_group:
  name: 'flink'
flink_user:
  name: 'flink'
  home: '/var/lib/flink'

flink_ssh_private_key: ''
flink_ssh_public_key: ''
flink_ssh_public_key_exclusive: True
flink_manage_known_hosts: True


# Service management
#------------------------------------------------------------------------------

flink_run_mode: 'local'

flink_service_description: 'Apache Flink'
flink_service_name: 'flink'
flink_service_state: 'started'
flink_service_enabled: True

# Systemd
flink_service_systemd:
  restart: 'on-failure'
  restart_sec: 1
  wanted_by: 'multi-user.target'


# Configuration
#------------------------------------------------------------------------------

flink_config: "{{ _flink_config }}"

_flink_config:
  jobmanager.heap.mb: 1024
  jobmanager.rpc.address: 'localhost'
  jobmanager.rpc.port: 6123
  jobmanager.web.address: '0.0.0.0'
  jobmanager.web.port: 8081
  jobmanager.web.submit.enable: False
  taskmanager.heap.mb: 1024
  taskmanager.memory.preallocate: False
  taskmanager.numberOfTaskSlots: 1
  parallelism.default: 1

flink_masters: []
flink_slaves: []
flink_additional_libs: []
```

### Debian OS family variables

``` yaml
_flink_system_dependencies:
  - name: 'unzip'
```

## Dependencies

No dependencies are hardcoded but need a valid Java installation.

For Xenial, use v8. With v9, Flink not start.


## Example Playbook

``` yaml
- hosts: servers
  roles:
    - { role: Temelio.flink }
```

## License

MIT

## Author Information

Alexandre Chaussier (for Temelio company)
- http://www.temelio.com
- alexandre.chaussier [at] temelio.com
