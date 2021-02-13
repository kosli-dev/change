from fingerprinters import Fingerprinter
import os
import subprocess

PROTOCOL = 'file://'


class FileFingerprinter(Fingerprinter):

    @property
    def notes(self):
        return "\n".join([
            f'The string `{PROTOCOL}` followed by the full path of the file to fingerprint.',
            'The full path must be volume-mounted.',
            'Example:',
            'docker run ... \\',
            f'    --env MERKELY_FINGERPRINT=”{PROTOCOL}${{YOUR_FILE_PATH}} \\',
            '    --volume=${YOUR_FILE_PATH}:${YOUR_FILE_PATH} \\',
            '    ...',
        ])

    @property
    def protocol(self):
        return PROTOCOL

    def handles_protocol(self, string):
        return string.startswith(PROTOCOL)

    def artifact_basename(self, string):
        return os.path.basename(self.artifact_name(string))

    def artifact_name(self, string):
        assert self.handles_protocol(string)
        return string[len(PROTOCOL):]

    def sha(self, string):
        assert self.handles_protocol(string)
        # Mocked in /tests/unit/utils/mock_file_fingerprinter.py
        # openssl is an Alpine package installed in /Dockerfile
        unrooted_filename = self.artifact_name(string)
        output = subprocess.check_output(["openssl", "dgst", "-sha256", '/'+unrooted_filename])
        digest_in_bytes = output.split()[1]
        return digest_in_bytes.decode('utf-8')
