from commands import *
import types

CI_NAMES = [ 'docker', 'github', 'bitbucket' ]


def test_doc_summary_for_all_commands():
    for command_name in Command.names():
        if command_name == 'control_pull_request':
            # Not on docs yet. Currently only supported on github
            continue
        summary = command_for(command_name).doc_summary()
        assert isinstance(summary, str), command_name
        assert len(summary) > 0, command_name


def test_doc_volume_mounts_for_all_commands():
    for command_name in Command.names():
        volume_mounts = command_for(command_name).doc_volume_mounts()
        assert type(volume_mounts) is list
        for volume_mount in volume_mounts:
            assert isinstance(volume_mount, str), command_name
            assert len(volume_mount) > 0, command_name


def command_for(name):
    cls = Command.named(name)
    env = {"MERKELY_COMMAND": name}
    return cls(External(env=env))
