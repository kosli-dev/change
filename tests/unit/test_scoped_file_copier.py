from os import path
import tempfile
from tests.utils import ScopedFileCopier
from pytest import raises


def test_copied_file_exists_only_inside_with_statement():
    filename = "jam.jar"
    source_path = f"/app/tests/data/{filename}"
    assert path.isfile(source_path)

    with tempfile.TemporaryDirectory() as dir_name:
        assert path.isdir(dir_name)
        target_path = f"{dir_name}/{filename}"
        assert not path.isfile(target_path)
        with ScopedFileCopier(source_path, target_path):
            assert path.isfile(target_path)

    assert not path.isfile(target_path)


def test_raises_when_source_file_does_not_exist():
    source_file = '/app/tests/data/does/not/exist.txt'
    assert not path.isfile(source_file)

    with raises(ScopedFileCopier.Error) as exc:
        ScopedFileCopier(source_file, 'any')

    assert str(exc.value) == f"source file '{source_file}' does not exist"
    assert not path.isfile(source_file)


def test_raises_when_target_file_already_exists():
    source_file = '/app/tests/data/jam.jar'
    assert path.isfile(source_file)

    with raises(ScopedFileCopier.Error) as exc:
        ScopedFileCopier(source_file, source_file)

    assert str(exc.value) == f"target file '{source_file}' already exists"
    assert path.isfile(source_file)
