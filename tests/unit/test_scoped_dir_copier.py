from os import path
from tests.utils import ScopedDirCopier

from pytest import raises


def test_target_dir_exists_in_with_statement_but_not_before_and_not_after():
    source_dir = '/app/tests/data/control_junit'
    target_dir = '/tmp/a/b/c'

    assert path.isdir(source_dir)
    assert not path.isdir(target_dir)

    with ScopedDirCopier(source_dir, target_dir):
        assert path.isdir(target_dir)

    assert not path.isdir(target_dir)


def test_source_dir_does_not_exist_raises():
    source_dir = '/app/tests/data/does/not/exist'
    target_dir = '/tmp/a/b/c'

    assert not path.isdir(source_dir)
    assert not path.isdir(target_dir)

    with raises(ScopedDirCopier.Error):
        with ScopedDirCopier(source_dir, target_dir):
            pass

    assert not path.isdir(source_dir)
    assert not path.isdir(target_dir)


def test_target_dir_already_exists_raises():
    source_dir = '/app/tests/data'
    target_dir = '/app/tests/data'

    assert path.isdir(source_dir)
    assert path.isdir(target_dir)

    with raises(ScopedDirCopier.Error):
        with ScopedDirCopier(source_dir, target_dir):
            pass

    assert path.isdir(source_dir)
    assert path.isdir(target_dir)
