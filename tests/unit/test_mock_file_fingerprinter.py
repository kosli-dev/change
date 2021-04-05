from tests.utils import MockFileFingerprinter
from pytest import raises

filename = 'jam.jar'
sha256 = '99032d90afaaa111e92920eea2b1abb0a6b6eafa6863ad7a4bd082a9c8574240'


def test_does_not_raise_when_expected_artifact_sha_arg():
    fingerprinter = MockFileFingerprinter(filename, sha256)
    fingerprinter.sha(f'file://{filename}')


def test_raises_when_unexpected_artifact_sha_arg():
    fingerprinter = MockFileFingerprinter(filename, sha256)
    with raises(RuntimeError) as exc:
        fingerprinter.sha(f'file://X{filename}')

    assert str(exc.value) == "\n".join([
        "MockFileFingerprinter.sha(string)",
        "FAILED",
        "Expected: string==jam.jar",
        "  Actual: string==Xjam.jar"
    ])


def test_raises_when_no_sha_call_inside_with_statement():
    with raises(RuntimeError) as exc:
        with MockFileFingerprinter(filename, sha256):
            pass

    assert str(exc.value) == "\n".join([
        "MockFileFingerprinter.sha(string)",
        "FAILED",
        "Expected sha() call did not happen",
        "exc_type = None",
        "exc_val = None"
    ])


def test_prints_exception_info_when_exception_trips_exit():
    with raises(RuntimeError) as exc:
        with MockFileFingerprinter(filename, sha256):
            raise RuntimeError("ABC")

    assert str(exc.value) == "\n".join([
        "MockFileFingerprinter.sha(string)",
        "FAILED",
        "Expected sha() call did not happen",
        "exc_type = <class 'RuntimeError'>",
        "exc_val = ABC"
    ])
