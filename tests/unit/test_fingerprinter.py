from errors import ChangeError
from fingerprinters import build_fingerprinter
from tests.utils import *
from pytest import raises

SHA256 = "ddee5566dc05772d90dc6929ad4f1fbc14aa105addf3326aa5cf575a104f51dc"


def test_builder__raises_when_name_is_unknown():
    with raises(ChangeError):
        build_fingerprinter('unknown')


def test_builder_does_not_raises_when_name_is_known():
    build_fingerprinter('docker_fingerprinter')


def test_fingerprinter__docker_image_sha():
    image_name = "acme/road-runner:4.8"
    fingerprinter = MockDockerFingerprinter(image_name, SHA256)
    assert fingerprinter.sha(f"docker://{image_name}") == SHA256


def test_fingerprint__file_at_root():
    filename = "jam.jar"
    fingerprinter = MockFileFingerprinter(filename, SHA256)
    assert fingerprinter.sha(f"file://{filename}") == SHA256


def test_fingerprint__file_in_directory():
    directory = "user/data"
    filename = "jam.jar"
    pathed = f"{directory}/{filename}"
    fingerprinter = MockFileFingerprinter(pathed, SHA256)
    assert fingerprinter.sha(f"file://{pathed}") == SHA256
