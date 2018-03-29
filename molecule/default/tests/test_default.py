import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_installed_packages(host):
    assert host.package('datadog-agent').is_installed


def test_files(host):
    integrations = [
        'elastic', 'go_expvar', 'gunicorn', 'kafka', 'php_fpm', 'nginx',
        'network', 'tcp_check', 'zk',
    ]
    for integration in integrations:
        assert host.file('/etc/dd-agent/conf.d/%s.yaml' % integration).exists

    for init_dir in ['/etc/rc0.d/', '/etc/rc6.d/']:
        assert host.file('%sK05datadog-agent' % init_dir).exists
        assert not host.file('%sK20datadog-agent' % init_dir).exists
