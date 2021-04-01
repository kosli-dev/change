from commands import run, Command, External
from errors import ChangeError
from tests.utils import *
from pytest import raises


def test_MEREKELY_OWNER_and_MERKELY_PIPE_LINE_are_used_for_all_commands_except_declare_pipeline():
    os_env = {
        "MERKELY_OWNER": "acme",
        "MERKELY_PIPELINE": "road-runner",
    }
    external = External(env=os_env)
    cls = Command.named('declare_pipeline')
    json = cls(external).merkelypipe
    assert json["owner"] == "acme"
    assert json["name"] == "road-runner"


def test_MERKELY_OWNER_and_MERKELY_PIPE_override_entries_in_Merkelypipe_even_for_declare_pipeline():
    # declare_pipeline requires a Merkelypipe.json file until its contents are 
    # provided on the server. Till then allow env-vars to override the "owner"
    # and "name" entries so that when anyone is doing the loan-calculator demo
    # they only need to set the values once in the env-vars for all commands.
    os_env = {
        "MERKELY_OWNER": "Acme",
        "MERKELY_PIPELINE": "road-runner-beep-beep",
    }
    external = External(env=os_env)
    cls = Command.named('declare_pipeline')
    with ScopedFileCopier('/app/tests/data/Merkelypipe.json', '/data/Merkelypipe.json'):
        json = cls(external).merkelypipe

    assert json["owner"] == "Acme"
    assert json["name"] == "road-runner-beep-beep"

    
def test_defaults_to_Merkelypipe_dot_json_in_data_dir():
    os_env = {}
    external = External(env=os_env)
    with ScopedFileCopier('/app/tests/data/Merkelypipe.json', '/data/Merkelypipe.json'):
        json = external.merkelypipe
    assert json['owner'] == 'merkely-test'


def test_env_var_can_override_the_default():
    os_env = {"MERKELY_PIPE_PATH": "/app/tests/data/Merkelypipe.acme-roadrunner.json"}
    external = External(env=os_env)
    json = external.merkelypipe
    assert json['owner'] == 'acme'


def test_raises_when_not_found(capsys):
    with dry_run(core_env_vars('log_artifact')) as env, raises(ChangeError):
        # no /data/Merkelypipe.json
        run(External(env=env))

    silence(capsys)

def test_raises_when_invalid_json(capsys):
    with dry_run(core_env_vars('log_artifact')) as env:
        external = External(env=env)
        with ScopedFileCopier("/app/tests/data/Merkelypipe.bad.json", "/Merkelypipe.json"):
            with raises(ChangeError):
                run(external)

    silence(capsys)


def test_raises_when_is_a_dir(capsys):
    with dry_run(core_env_vars('log_artifact')) as env:
        external = External(env=env)
        with ScopedDirCopier("/app/tests/data", "/data/Merkelypipe.json"):
            with raises(ChangeError):
                run(external)
    silence(capsys)

"""
Possible further tests:
TODO: json has no key "owner"
TODO: json "owner" value not string
"""
