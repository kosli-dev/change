from errors import ChangeError
from fingerprinters import Fingerprinter
import os
import subprocess
import tempfile

PROTOCOL = 'dir://'


NOTES = " ".join([
    f'To fingerprint a dir use the string :code:`{PROTOCOL}` followed by',
    'the full path of the dir to fingerprint.',
    'The command will calculate the sha digest.',
    'The full path must be volume-mounted.',
])


EXAMPLE = "\n".join([
    'docker run \\',
    '    ...',
    f'    --env MERKELY_FINGERPRINT=”{PROTOCOL}${{YOUR_DIR_PATH}} \\',
    '    --volume=${YOUR_DIR_PATH}:${YOUR_DIR_PATH} \\',
    '    ...',
])


class DirFingerprinter(Fingerprinter):

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
        # openssl is an Alpine package installed in /Dockerfile
        dir_name = self.artifact_name(string)
        tmp_dir = tempfile.mkdtemp()
        with open(f"{tmp_dir}/digests", "a+") as digest_file:
            dir_sha256(f"/{dir_name}", digest_file, tmp_dir)
        
        return sha256(f"{tmp_dir}/digests")


def sha256(filepath):
    output = subprocess.check_output(["openssl", "dgst", "-sha256", filepath])
    digest_in_bytes = output.split()[1]
    return digest_in_bytes.decode('utf-8')


def append_sha256(digest_file, name, tmp_dir):
    with open(f"{tmp_dir}/name", "w+") as file:
        file.write(name)
    digest_file.write(sha256(f"{tmp_dir}/name"))


def dir_sha256(dir_name, digest_file, tmp_dir):
    append_sha256(digest_file, dir_name, tmp_dir)

    entries = [entry for entry in os.listdir(dir_name)]
    for entry in sorted(entries):
        pathed_entry = os.path.join(dir_name, entry)
        if os.path.isfile(pathed_entry):
            append_sha256(digest_file, pathed_entry, tmp_dir)
            digest_file.write(sha256(pathed_entry))
        else:
            dir_sha256(pathed_entry, digest_file, tmp_dir)