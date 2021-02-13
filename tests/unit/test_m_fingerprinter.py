from fingerprinters import Sha256Fingerprinter
from tests.utils import *

SHA256 = "ddee5566dc05772d90dc6929ad4f1fbc14aa105addf3326aa5cf575a104f51dc"


def test_fingerprinter__docker_image_sha():
    image_name = "acme/road-runner:4.8"
    env_var = f"docker://{image_name}"
    fingerprinter = MockDockerFingerprinter(image_name, SHA256)
    assert fingerprinter.sha(image_name) == SHA256


def test_fingerprint__file_at_root():
    filename = "jam.jar"
    fingerprinter = MockFileFingerprinter(filename, SHA256)
    assert fingerprinter.sha(filename) == SHA256


def test_fingerprint__file_in_directory():
    directory = "user/data"
    filename = "jam.jar"
    pathed = f"{directory}/{filename}"
    fingerprinter = MockFileFingerprinter(pathed, SHA256)
    assert fingerprinter.sha(pathed) == SHA256
