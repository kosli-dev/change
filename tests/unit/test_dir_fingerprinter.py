from errors import ChangeError
from fingerprinters import DirFingerprinter
from pytest import raises
import os
import shutil

DIR_PROTOCOL = "dir://"


def test_non_existing_dir_error_message():
    fingerprinter = DirFingerprinter()
    basename = "c"
    path = "a/b/c"
    string = f"{DIR_PROTOCOL}{path}"
    assert fingerprinter.artifact_name(string) == path
    assert fingerprinter.artifact_basename(string) == basename
    with raises(ChangeError) as exc:
        fingerprinter.sha(string)
    assert str(exc.value) == "No such directory: '/a/b/c'"


def test_empty_dir_properties(tmp_path):
    fingerprinter = DirFingerprinter()
    basename = "test_empty_dir_properties0"
    path = str(tmp_path)
    string = f"{DIR_PROTOCOL}{path}"
    assert fingerprinter.artifact_name(string) == path
    assert fingerprinter.artifact_basename(string) == basename
    assert fingerprinter.sha(string) == '0e64e0a7586808ddf0b4e12487006de037b13a3baec4b80293f012b49b84fdeb'


def test_dir_with_one_file_with_known_content():
    fingerprinter = DirFingerprinter()
    dir = f"tmp/test_dir_with_one_file_with_known_content"

    os.mkdir(f"/{dir}")
    with open(f"/{dir}/file.extra", "w+") as file:
        file.write("this is known extra content")

    assert fingerprinter.sha(f"{DIR_PROTOCOL}{dir}") == '9b9d0a0f475c2e94e21a10a5d05438783bd1effeda27d55ef4f766c8e2c715b2'
    shutil.rmtree(f"/{dir}")


def test_handles_only_its_own_protocol():
    fingerprinter = DirFingerprinter()
    assert fingerprinter.handles_protocol(DIR_PROTOCOL)
    assert not fingerprinter.handles_protocol('X'+DIR_PROTOCOL)


def test_notes_and_example_docs_are_set():
    fingerprinter = DirFingerprinter()
    assert len(fingerprinter.notes) > 0
    assert len(fingerprinter.example) > 0


def test_directory_not_specified_raises():
    fingerprinter = DirFingerprinter()
    dir_name = ""
    string = DIR_PROTOCOL + dir_name
    def assert_raises(method_name):
        with raises(ChangeError) as exc:
            getattr(fingerprinter, method_name)(string)
        assert str(exc.value) == f"Empty {DIR_PROTOCOL} fingerprint"

    assert_raises('artifact_name')
    assert_raises('artifact_basename')
    assert_raises('sha')


def test_non_empty_dir_properties():
    fingerprinter = DirFingerprinter()
    basename = "control_junit"
    path = f"app/tests/data/{basename}"
    string = f"{DIR_PROTOCOL}{path}"
    assert fingerprinter.artifact_name(string) == path
    assert fingerprinter.artifact_basename(string) == basename
    assert fingerprinter.sha(string) == '8eff10fe50ce2e5f5df04aea3b6f805c3d3e4d9828b27d87d19aef14806d9d60'


def test_different_non_empty_dir_properties():
    fingerprinter = DirFingerprinter()
    basename = "control_junit"
    path = f"app/tests/data/{basename}"
    with open(f"/{path}/extra.file", "w+") as file:
        file.write("any extra content")
    string = f"{DIR_PROTOCOL}{path}"
    assert fingerprinter.artifact_name(string) == path
    assert fingerprinter.artifact_basename(string) == basename
    assert fingerprinter.sha(string) == 'eb7dc9fcf956aecad5484b35adc330a5a7718620ee8cbc64f0d223bc95a90d35'

    os.remove(f"/{path}/extra.file")
