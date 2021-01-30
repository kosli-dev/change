import docker
import os
import subprocess


def sha_digest_for_file(pathed_filename):
    output = subprocess.check_output(["openssl", "dgst", "-sha256", pathed_filename])
    digest_in_bytes = output.split()[1]
    artifact_sha = digest_in_bytes.decode('utf-8')
    return artifact_sha


def sha_digest_for_docker_image(docker_image_name):
    client = docker.from_env()
    print("Inspecting docker image for sha256Digest")
    image = client.images.get(docker_image_name)
    repo_digest = image.attrs["RepoDigests"][0].split(":")[1]
    return repo_digest


if __name__ == '__main__':
    from command_processor import execute
    context = {
        'env': os.environ,
        'sha_digest_for_file': sha_digest_for_file,
        'sha_digest_for_docker_image': sha_digest_for_docker_image
    }
    execute(context)
