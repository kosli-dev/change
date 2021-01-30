import os
import subprocess


def sha_digest_for_file(artifact_path):
    output = subprocess.check_output(["openssl", "dgst", "-sha256", artifact_path])
    digest_in_bytes = output.split()[1]
    artifact_sha = digest_in_bytes.decode('utf-8')
    return artifact_sha


if __name__ == '__main__':
    from command_processor import execute
    context = {
        'env': os.environ,
        'sha_digest_file_file': sha_digest_file_file
    }
    execute(context)
