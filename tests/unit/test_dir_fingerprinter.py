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
    assert fingerprinter.sha(string) == 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'


def test_dir_with_one_file_with_known_content():
    fingerprinter = DirFingerprinter()
    dir = f"tmp/test_single_dir_with_one_file_with_known_content"

    os.mkdir(f"/{dir}")
    with open(f"/{dir}/file.extra", "w+") as file:
        file.write("this is known extra content")

    assert fingerprinter.sha(f"{DIR_PROTOCOL}{dir}") == 'c71f5baef8cce289c9b7c971cf219e21b787a025af68ad6539b82634fe62819e'
    shutil.rmtree(f"/{dir}")


def test_digest_is_the_same_for_same_content_in_different_root_directories():
    fingerprinter = DirFingerprinter()

    dir = f"tmp/test_dir_with_one_file_with_known_content"
    os.mkdir(f"/{dir}")
    with open(f"/{dir}/file.extra", "w+") as file:
        file.write("this is known extra content")
    assert fingerprinter.sha(f"{DIR_PROTOCOL}{dir}") == 'c71f5baef8cce289c9b7c971cf219e21b787a025af68ad6539b82634fe62819e'
    shutil.rmtree(f"/{dir}")

    different_dir = f"tmp/test_different_dir_with_one_file_with_known_content"
    os.mkdir(f"/{different_dir}")
    with open(f"/{different_dir}/file.extra", "w+") as file:
        file.write("this is known extra content")
    assert fingerprinter.sha(f"{DIR_PROTOCOL}{different_dir}") == 'c71f5baef8cce289c9b7c971cf219e21b787a025af68ad6539b82634fe62819e'
    shutil.rmtree(f"/{different_dir}")


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
    assert fingerprinter.sha(string) == '4ca24dede15db858aae709933ef48f16031a89a356a6f5d29dd2140a1e3c8313'


def test_different_non_empty_dir_properties():
    try:
        fingerprinter = DirFingerprinter()
        basename = "control_junit"
        path = f"app/tests/data/{basename}"
        with open(f"/{path}/extra.file", "w+") as file:
            file.write("any extra content")
        string = f"{DIR_PROTOCOL}{path}"
        assert fingerprinter.artifact_name(string) == path
        assert fingerprinter.artifact_basename(string) == basename
        assert fingerprinter.sha(string) == 'c8c29f1766aba2cf654b4bbf8e372d334180d5762376a8247773e6d5f0ac93c6'
    finally:
        os.remove(f"/{path}/extra.file")