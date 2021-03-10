from commands import run, External
from errors import ChangeError
from tests.utils import *
from pytest import raises


def test_defaults_to_Merkelypipe_dot_json_in_data_dir():
    os_env = {}
    external = External(env=os_env)
    with ScopedFileCopier('/app/tests/data/Merkelypipe.json', '/data/Merkelypipe.json'):
        json = external.merkelypipe
    assert json['owner'] == 'merkely-test'


def test_env_var_can_override_the_default():
    os_env = {"MERKELYPIPE_PATH": "/app/tests/data/Merkelypipe.acme-roadrunner.json"}
    external = External(env=os_env)
    json = external.merkelypipe
    assert json['owner'] == 'acme'


def test_raises_when_not_found(capsys):
    with dry_run(core_env_vars()) as env, raises(ChangeError):
        # no /data/Merkelypipe.json
        run(External(env=env))


def test_raises_when_invalid_json(capsys):
    with dry_run(core_env_vars()) as env:
        external = External(env=env)
        with ScopedFileCopier("/app/tests/data/Merkelypipe.bad.json", "/Merkelypipe.json"):
            with raises(ChangeError):
                run(external)


def test_raises_when_is_a_dir(capsys):
    with dry_run(core_env_vars()) as env:
        external = External(env=env)
        with ScopedDirCopier("/test_src", "/Merkelypipe.json"):
            with raises(ChangeError):
                run(external)


"""
Possible further tests:

json has no key "owner"
json "owner" value not string
"""
