from errors import ChangeError
from fingerprinters import Fingerprinter
import os
import subprocess

PROTOCOL = 'file://'


NOTES = " ".join([
    f'To fingerprint a file use the string :code:`{PROTOCOL}` followed by',
    'the full path of the file to fingerprint.',
    'The command will calculate the sha digest.',
    'The full path must be volume-mounted.',
])


EXAMPLE = "\n".join([
    'docker run \\',
    '    ...',
    f'    --env MERKELY_FINGERPRINT=”{PROTOCOL}${{YOUR_FILE_PATH}} \\',
    '    --volume=${YOUR_FILE_PATH}:${YOUR_FILE_PATH} \\',
    '    ...',
])


class FileFingerprinter(Fingerprinter):

    @property
    def notes(self):
        return NOTES

    @property
    def example(self):
        return EXAMPLE

    def handles_protocol(self, string):
        return string.startswith(PROTOCOL)

    def artifact_basename(self, string):
        return os.path.basename(self.artifact_name(string))

    def artifact_name(self, string):
        assert self.handles_protocol(string)
        result = string[len(PROTOCOL):]
        if result == "":
            raise ChangeError(f"Empty {PROTOCOL} fingerprint")
        return result

    def sha(self, string):
        assert self.handles_protocol(string)
        # Mocked in /tests/unit/utils/mock_file_fingerprinter.py
        # openssl is an Alpine package installed in /Dockerfile
        unrooted_filename = self.artifact_name(string)
        if not os.path.isfile("/" + unrooted_filename):
            raise ChangeError(f"No such file: '{unrooted_filename}'")
        output = subprocess.check_output(["openssl", "dgst", "-sha256", '/'+unrooted_filename])
        digest_in_bytes = output.split()[1]
        return digest_in_bytes.decode('utf-8')
