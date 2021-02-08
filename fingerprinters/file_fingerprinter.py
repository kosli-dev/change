from fingerprinters import Fingerprinter
import subprocess


class FileFingerprinter(Fingerprinter):

    def _fingerprint(self, pathed_filename):
        # Mocked in /tests/unit/utils/mock_file_fingerprinter.py
        # openssl is an Alpine package installed in /Dockerfile
        output = subprocess.check_output(["openssl", "dgst", "-sha256", '/'+pathed_filename])
        digest_in_bytes = output.split()[1]
        return digest_in_bytes.decode('utf-8')
