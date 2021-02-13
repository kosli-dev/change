from tests.utils import *

SHA256 = "ddee5566dc05772d90dc6929ad4f1fbc14aa105addf3326aa5cf575a104f51dc"


def test_docker_fingerprint():
    image_name = "acme/road-runner:4.8"
    fingerprinter = MockDockerFingerprinter(image_name, SHA256)
    assert fingerprinter.sha(image_name) == SHA256


def test_file_fingerprint():
    filename = "jam.jar"
    fingerprinter = MockFileFingerprinter(filename, SHA256)
    assert fingerprinter.sha(filename) == SHA256
