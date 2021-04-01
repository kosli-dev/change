from commands import Command
from errors import ChangeError
from pytest import raises


def test_command_named():
    klass = Command.named('log_artifact')
    assert klass.__name__ == 'LogArtifact'
    klass = Command.named('request_approval')
    assert klass.__name__ == 'RequestApproval'


def test_command_named_raises_when_unknown():
    with raises(ChangeError) as exc:
        Command.named('xyz')
    assert str(exc.value) == 'Unknown command: xyz'


def test_known_command_names():
    names = (Command.names())
    assert 'declare_pipeline' in names
    assert 'log_artifact' in names
