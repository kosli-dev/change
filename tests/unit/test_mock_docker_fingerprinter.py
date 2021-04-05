from tests.utils import MockDockerFingerprinter
from pytest import raises

image_name = 'acme/road-runner:2.3'
sha256 = '13032d90afaaa111e92920eea2b1abb0a6b6eafa6863ad7a4bd082a9c8574240'


def test_does_not_raise_when_expected_artifact_sha_arg():
    fingerprinter = MockDockerFingerprinter(image_name, sha256)
    fingerprinter.sha(f'docker://{image_name}')


def test_raises_when_unexpected_artifact_sha_arg():
    fingerprinter = MockDockerFingerprinter(image_name, sha256)
    with raises(RuntimeError) as exc:
        fingerprinter.sha(f'docker://X{image_name}')

    assert str(exc.value) == "\n".join([
        "MockDockerFingerprinter.sha(string)",
        "FAILED",
        "Expected: string==acme/road-runner:2.3",
        "  Actual: string==Xacme/road-runner:2.3"
    ])


def test_raises_when_no_sha_call_inside_with_statement():
    with raises(RuntimeError) as exc:
        with MockDockerFingerprinter(image_name, sha256):
            pass

    assert str(exc.value) == "\n".join([
        "MockDockerFingerprinter.sha(string)",
        "FAILED",
        "Expected sha() call did not happen",
        "exc_type = None",
        "exc_val = None"
    ])


def test_prints_exception_info_when_exception_trips_exit():
    with raises(RuntimeError) as exc:
        with MockDockerFingerprinter(image_name, sha256):
            raise RuntimeError("ABC")

    assert str(exc.value) == "\n".join([
        "MockDockerFingerprinter.sha(string)",
        "FAILED",
        "Expected sha() call did not happen",
        "exc_type = <class 'RuntimeError'>",
        "exc_val = ABC"
    ])
