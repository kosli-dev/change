from errors import ChangeError
from fingerprinters import Fingerprinter
import os
import subprocess
import tempfile
import shutil


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
        dir_name = '/' + self.artifact_name(string)
        if not os.path.isdir(dir_name):
            raise ChangeError(f"No such directory: '{dir_name}'")

        tmp_dir = tempfile.mkdtemp()
        with open(f"{tmp_dir}/digests", "a+") as digest_file:
            dir_sha256(digest_file, dir_name, tmp_dir)
        result = sha256(f"{tmp_dir}/digests")
        shutil.rmtree(tmp_dir)
        return result


def sha256(filepath):
    # openssl is an Alpine package installed in /Dockerfile
    output = subprocess.check_output(["openssl", "dgst", "-sha256", filepath])
    digest_in_bytes = output.split()[1]
    return digest_in_bytes.decode('utf-8')


def append_sha256(digest_file, full_path, tmp_dir):
    with open(f"{tmp_dir}/name", "w+") as file:
        # Basename is used so that the sha256 remains the same
        # if the directory structure is moved to a different
        # base directory
        file.write(os.path.basename(full_path))
    digest_file.write(sha256(f"{tmp_dir}/name"))


def dir_sha256(digest_file, dir_name, tmp_dir):

    entries = [entry for entry in os.listdir(dir_name)]
    for entry in sorted(entries):
        pathed_entry = os.path.join(dir_name, entry)
        if os.path.isfile(pathed_entry):
            append_sha256(digest_file, pathed_entry, tmp_dir)
            digest_file.write(sha256(pathed_entry))
        else:
            append_sha256(digest_file, dir_name, tmp_dir)
            dir_sha256(digest_file, pathed_entry, tmp_dir)