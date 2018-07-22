import os

from napalm.base import exceptions

from nornir.plugins.tasks import networking


THIS_DIR = os.path.dirname(os.path.realpath(__file__)) + "/mocked/napalm_configure"


def connect(task, connection_options):
    task.host.open_connection(
        "napalm",
        hostname=task.host.username,
        password=task.host.password,
        network_api_port=task.host.network_api_port,
        nos=task.host.nos,
        connection_options=connection_options,
    )


class Test(object):
    def test_napalm_configure_change_dry_run(self, nornir):
        opt = {"path": THIS_DIR + "/test_napalm_configure_change_dry_run"}
        configuration = "hostname changed-hostname"
        d = nornir.filter(name="dev3.group_2")
        d.run(connect, connection_options=opt)
        result = d.run(networking.napalm_configure, configuration=configuration)
        assert result
        for h, r in result.items():
            assert "+hostname changed-hostname" in r.diff
            assert r.changed

    def test_napalm_configure_change_commit(self, nornir):
        opt = {"path": THIS_DIR + "/test_napalm_configure_change_commit/step1"}
        configuration = "hostname changed-hostname"
        d = nornir.filter(name="dev3.group_2")
        d.run(connect, connection_options=opt)
        result = d.run(
            networking.napalm_configure, dry_run=False, configuration=configuration
        )
        assert result
        for h, r in result.items():
            assert "+hostname changed-hostname" in r.diff
            assert r.changed
        opt = {"path": THIS_DIR + "/test_napalm_configure_change_commit/step2"}
        d.run(connect, connection_options=opt)
        result = d.run(
            networking.napalm_configure, dry_run=True, configuration=configuration
        )
        assert result
        for h, r in result.items():
            assert "+hostname changed-hostname" not in r.diff
            assert not r.changed

    def test_napalm_configure_change_error(self, nornir):
        opt = {"path": THIS_DIR + "/test_napalm_configure_change_error"}
        configuration = "hostname changed_hostname"

        d = nornir.filter(name="dev3.group_2")
        d.run(connect, connection_options=opt)
        results = d.run(networking.napalm_configure, configuration=configuration)
        processed = False
        for result in results.values():
            processed = True
            assert isinstance(result.exception, exceptions.MergeConfigException)
        assert processed
        nornir.data.reset_failed_hosts()
