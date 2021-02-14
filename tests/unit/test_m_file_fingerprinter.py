from commands import CommandError
from fingerprinters import FileFingerprinter
from pytest import raises

FILE_PROTOCOL = "file://"


def test_handles_only_its_own_protocol():
    fingerprinter = FileFingerprinter()
    assert fingerprinter.handles_protocol(FILE_PROTOCOL)
    assert not fingerprinter.handles_protocol('X'+FILE_PROTOCOL)


def test_non_empty_filename_properties():
    fingerprinter = FileFingerprinter()
    basename = "jam.jar"
    path = f"user/artifact/{basename}"
    string = f"{FILE_PROTOCOL}{path}"
    assert fingerprinter.artifact_name(string) == path
    assert fingerprinter.artifact_basename(string) == basename


def test_empty_filename_raises():
    fingerprinter = FileFingerprinter()
    filename = ""
    string = FILE_PROTOCOL + filename
    def assert_raises(method_name):
        with raises(CommandError) as exc:
            getattr(fingerprinter, method_name)(string)
        assert str(exc.value) == f"Empty {FILE_PROTOCOL} fingerprint"

    assert_raises('artifact_name')
    assert_raises('artifact_basename')
