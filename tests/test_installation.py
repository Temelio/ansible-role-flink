"""
Role tests
"""

import pytest
from testinfra.utils.ansible_runner import AnsibleRunner

testinfra_hosts = AnsibleRunner('.molecule/ansible_inventory').get_hosts('all')


def test_user(host):
    """
    Test user settings
    """

    flink_user = host.user('flink')
    assert flink_user.exists
    assert flink_user.group == 'flink'
    assert flink_user.home == '/var/lib/flink'


@pytest.mark.parametrize('path_type,path,user,group,mode', [
    ('directory', '/var/lib/flink', 'flink', 'flink', 0o750),
    ('symlink', '/var/lib/flink/current', 'flink', 'flink', 0o777),
    ('directory', '/var/lib/flink/current/conf', 'flink', 'flink', 0o775),
    ('directory', '/var/log/flink', 'flink', 'flink', 0o750),
    ('directory', '/var/run/flink', 'flink', 'flink', 0o750),
    (
        'file', '/var/lib/flink/current/conf/flink-conf.yaml', 'flink',
        'flink', 0o400
    ),
    ('file', '/var/lib/flink/current/conf/masters', 'flink', 'flink', 0o644),
    ('file', '/var/lib/flink/current/conf/slaves', 'flink', 'flink', 0o400),
])
def test_files_and_folders(host, path_type, path, user, group, mode):
    """
    Ensure needed folders exists
    """

    current_path = host.file(path)

    assert current_path.exists
    assert current_path.user == user
    assert current_path.group == group
    assert current_path.mode == mode

    if path_type == 'directory':
        assert current_path.is_directory
    elif path_type == 'file':
        assert current_path.is_file
    elif path_type == 'symlink':
        assert current_path.is_symlink


@pytest.mark.parametrize('path,user,group,mode,codenames', [
    ('/etc/systemd/system/flink.service', 'root', 'root', 0o644, ['xenial']),
    ('/etc/init.d/flink', 'root', 'root', 0o755, ['trusty']),
])
def test_service_file(host, path, user, group, mode, codenames):
    """
    Ensure service file exists
    """

    if host.system_info.codename not in codenames:
        pytest.skip('Not apply to this distribution')

    current_path = host.file(path)

    assert current_path.exists
    assert current_path.is_file
    assert current_path.user == user
    assert current_path.group == group
    assert current_path.mode == mode


def test_service(host):
    """
    Ensure service managed and running
    """

    flink_service = host.service('flink')

    assert flink_service.is_enabled
    assert flink_service.is_running


def test_socket(host):
    """
    Ensure flink socket listening
    """

    assert host.socket('tcp://0.0.0.0:8081').is_listening
