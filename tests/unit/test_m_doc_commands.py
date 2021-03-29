from commands import *
import types

CI_NAMES = [ 'docker', 'github', 'bitbucket' ]


def test_doc_summary_for_all_commands():
    for command_name in Command.names():
        for ci_name in CI_NAMES:
            summary = command_for(command_name).doc_summary(ci_name)
            assert isinstance(summary, str)


def test_doc_volume_mounts_for_all_commands():
    for command_name in Command.names():
        for ci_name in CI_NAMES:
            volume_mounts = command_for(command_name).doc_volume_mounts(ci_name)
            for volume_mount in volume_mounts:
                assert isinstance(volume_mount, str)


def command_for(name):
    cls = Command.named(name)
    env = {"MERKELY_COMMAND": name}
    return cls(External(env=env))
