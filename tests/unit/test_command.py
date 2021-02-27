from commands import Command
from errors import ChangeError
from pytest import raises


def test_command_named():
    klass = Command.named('log_artifact')
    assert klass.__name__ == 'LogArtifact'
    klass = Command.named('log_approval')
    assert klass.__name__ == 'LogApproval'


def test_command_named_raises_when_unknown():
    with raises(ChangeError) as exc:
        Command.named('xyz')
    assert str(exc.value) == 'Unknown command: xyz'


def test_command_class_iteration():
    names = list(name for name in Command.all().keys())
    assert 'DeclarePipeline' in names
    assert 'LogArtifact' in names
