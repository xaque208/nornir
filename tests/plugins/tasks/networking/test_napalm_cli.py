import os

#  from nornir.core.exceptions import NornirExecutionError
from nornir.plugins.tasks import networking

#  from napalm.base import exceptions

#  import pytest


THIS_DIR = os.path.dirname(os.path.realpath(__file__)) + "/mocked/napalm_cli"


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
    def test_napalm_cli(self, nornir):
        opt = {"path": THIS_DIR + "/test_napalm_cli"}
        d = nornir.filter(name="dev3.group_2")
        d.run(connect, connection_options=opt)
        result = d.run(
            networking.napalm_cli, commands=["show version", "show interfaces"]
        )
        assert result
        for h, r in result.items():
            assert r.result["show version"]
            assert r.result["show interfaces"]


#  def test_napalm_cli_error(self, nornir):
#      opt = {"path": THIS_DIR + "/test_napalm_cli_error"}
#      with pytest.raises(NornirExecutionError) as e:
#          nornir.filter(name="dev3.group_2").run(networking.napalm_cli,
#                                                  num_workers=1,
#                                                  commands=["show version",
#                                                            "show interfacesa"],
#                                                  optional_args=opt)
#      assert len(e.value.failed_hosts)
#      for result in e.value.failed_hosts.values():
#          assert isinstance(result.exception, exceptions.CommandErrorException)
#          print(exc)
