from commands import *
import types

CI_NAMES = [ 'docker', 'github', 'bitbucket' ]

def test_doc_example_for_all_env_vars():
    for command_name in Command.names():
        command = command_for(command_name)
        for var in command.merkely_env_vars:
            for ci_name in CI_NAMES:
                ok, eg = var.doc_example(ci_name, command_name)
                assert ok is True or ok is False
                assert isinstance(eg, str)


def test_doc_note_for_all_env_vars():
    for command_name in Command.names():
        command = command_for(command_name)
        for var in command.merkely_env_vars:
            for ci_name in CI_NAMES:
                note = var.doc_note(ci_name, command_name)
                assert isinstance(note, str)


def command_for(name):
    cls = Command.named(name)
    env = {"MERKELY_COMMAND": name}
    return cls(External(env=env))
