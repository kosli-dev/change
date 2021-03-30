from errors import ChangeError
from fingerprinters import FileFingerprinter
from pytest import raises

FILE_PROTOCOL = "file://"


def test_non_empty_filename_properties():
    fingerprinter = FileFingerprinter()
    basename = "jam.jar"
    path = f"app/tests/data/{basename}"
    string = f"{FILE_PROTOCOL}{path}"
    assert fingerprinter.artifact_name(string) == path
    assert fingerprinter.artifact_basename(string) == basename
    assert fingerprinter.sha(string) == 'ccee89ccdc05772d90dc6929ad4f1fbc14aa105addf3326aa5cf575a104f51dc'


def test_handles_only_its_own_protocol():
    fingerprinter = FileFingerprinter()
    assert fingerprinter.handles_protocol(FILE_PROTOCOL)
    assert not fingerprinter.handles_protocol('X'+FILE_PROTOCOL)


def test_notes_and_example_docs_are_set():
    fingerprinter = FileFingerprinter()
    assert len(fingerprinter.notes) > 0
    assert len(fingerprinter.example) > 0


def test_empty_filename_raises():
    fingerprinter = FileFingerprinter()
    filename = ""
    string = FILE_PROTOCOL + filename
    def assert_raises(method_name):
        with raises(ChangeError) as exc:
            getattr(fingerprinter, method_name)(string)
        assert str(exc.value) == f"Empty {FILE_PROTOCOL} fingerprint"

    assert_raises('artifact_name')
    assert_raises('artifact_basename')
    assert_raises('sha')
