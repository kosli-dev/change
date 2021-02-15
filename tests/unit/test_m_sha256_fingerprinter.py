from commands import CommandError
from fingerprinters import Sha256Fingerprinter
from pytest import raises

SHA256_PROTOCOL = 'sha256://'
SHA256 = "ddee5566dc05772d90dc6929ad4f1fbc14aa105addf3326aa5cf575a104f51dc"


def test_sha256_protocol__valid_sha_and_non_empty_artifact_name_properties():
    image_name = "acme/road-runner:2.34"
    fingerprinter = Sha256Fingerprinter()
    string = f'sha256://{SHA256}/{image_name}'
    assert fingerprinter.handles_protocol(string)
    assert fingerprinter.artifact_name(string) == image_name
    assert fingerprinter.artifact_basename(string) == image_name


def test_notes_and_example_docs_are_set():
    fingerprinter = Sha256Fingerprinter()
    assert len(fingerprinter.notes) > 0
    assert len(fingerprinter.example) > 0


def test_sha256_protocol__bad_sha_raises():
    bad_shas = [
        "",   # empty
        'a',  # too short by a lot
        SHA256[0:-1],  # too short by 1
        SHA256+'0',  # too long by 1
        SHA256+'0123456789abcdef',  # too long by a lot
        SHA256[0:-1]+'F',  # bad last char
        'E'+SHA256[1:],  # bad first char
        ('4'*32) + 'B' + ('5'*31),  # bad middle char
    ]
    for bad_sha in bad_shas:
        image_name = "acme/road-runner:2.34"
        fingerprinter = Sha256Fingerprinter()
        string = f"sha256://{bad_sha}/{image_name}"
        with raises(CommandError) as exc:
            fingerprinter.sha(string)
        assert str(exc.value) == f"Invalid {SHA256_PROTOCOL} fingerprint: {bad_sha}/{image_name}"


def test_sha256_protocol__no_artifact_name_raises():
    no_slash = ''
    empty = '/'
    for bad in [no_slash, empty]:
        fingerprinter = Sha256Fingerprinter()
        string = f"sha256://{SHA256}{bad}"
        with raises(CommandError) as exc:
            fingerprinter.artifact_name(string)
        assert str(exc.value) == f"Invalid {SHA256_PROTOCOL} fingerprint: {SHA256}{bad}"


