from commands import External
from errors import ChangeError
from fingerprinters import *
import os
from pytest import raises


def test_env_defaults_to_os_environ():
    external = External()
    assert external.env is os.environ


def test_docker_fingerprinter_defaults_to_DockerFingerprinter():
    external = External()
    assert isinstance(external.fingerprinter_for('docker://'), DockerFingerprinter)


def test_file_fingerprinter_defaults_to_FileFingerprinter():
    external = External()
    assert isinstance(external.fingerprinter_for('file://'), FileFingerprinter)


def test_sha256_fingerprinter_defaults_to_FileFingerprinter():
    external = External()
    assert isinstance(external.fingerprinter_for('sha256://'), Sha256Fingerprinter)


def test_load_json_raises_when_file_not_found():
    external = External()
    bad_filename = '/a/b/c.json'
    with raises(ChangeError) as exc:
        external.load_json(bad_filename)
    assert str(exc.value) == f"{bad_filename} file not found."


def test_load_json_raises_when_file_is_a_dir():
    external = External()
    dir_name = '/app'
    with raises(ChangeError) as exc:
        external.load_json(dir_name)
    assert str(exc.value) == f"{dir_name} is a directory."


def test_load_json_raises_when_file_contains_bad_json():
    external = External()
    not_json = '/app/tests/data/README.md'
    with raises(ChangeError) as exc:
        external.load_json(not_json)
    assert str(exc.value) == f"{not_json} invalid json - Expecting value: line 1 column 1 (char 0)"
