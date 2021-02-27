from commands import build_command, Command
from errors import ChangeError
from pytest import raises

def test_build_command():
    klass = build_command('log_artifact')
    assert klass.__name__ == 'LogArtifact'
    klass = build_command('log_approval')
    assert klass.__name__ == 'LogApproval'

def test_build_command_raises_when_unknown():
    with raises(ChangeError) as exc:
        build_command('xyz')
    assert str(exc.value) == 'Unknown command: xyz'

def test_command_create():
    klass = Command.create('log_artifact')
    assert klass.__name__ == 'LogArtifact'
    klass = Command.create('log_approval')
    assert klass.__name__ == 'LogApproval'

def test_command_raises_when_unknown():
    with raises(ChangeError) as exc:
        Command.create('xyz')
    assert str(exc.value) == 'Unknown command: xyz'
