from cdb.api_schema import ApiSchema
from cdb.http import http_put_payload


def execute(env):
    command = env.get("MERKELY_COMMAND", None)
    print("MERKELY_COMMAND={}".format(command))
    merkleypipe_path = "/Merkelypipe.json"
    with open(merkleypipe_path) as merkelypipe_file:
        merkelypipe = load_merkelypipe(merkelypipe_file)
        api_token = env.get('MERKELY_API_TOKEN', None)
        host = "https://app.compliancedb.com"
        if command == "declare_pipeline":
            declare_pipeline(env, merkelypipe, api_token, host)
        if command == "log_artifact":
            log_artifact(env, merkelypipe, api_token, host)

    return 0


def declare_pipeline(env, merkelypipe, api_token, host):
    pipelines_url = ApiSchema.url_for_pipelines(host, merkelypipe)
    http_put_payload(url=pipelines_url, payload=merkelypipe, api_token=api_token)


def log_artifact(env, merkelypipe, api_token, host):
    fingerprint = env.get("MERKELY_FINGERPRINT", None)
    protocol = fingerprint[:len("file://")]
    artifact_name = '/' + fingerprint[len("file://"):]
    print("Getting SHA for artifact: " + artifact_name)  # print "file" ?
    artifact_sha = sha_digest_for_file(artifact_name)
    print("Calculated digest: " + artifact_sha)
    #print("Publish artifact to ComplianceDB")
    description = "Created by build " + env.get('MERKELY_CI_BUILD_NUMBER', None)
    git_commit = env.get('MERKELY_ARTIFACT_GIT_COMMIT', None)
    commit_url = env.get('MERKELY_ARTIFACT_GIT_URL', None)
    build_url = env.get('MERKELY_CI_BUILD_URL', None)
    # is_compliant = env_is_compliant()
    # print('CDB_IS_COMPLIANT: ' + str(is_compliant))
    create_artifact(api_token, host, merkelypipe,
                    artifact_sha, artifact_name,
                    description, git_commit, commit_url, build_url)


import json
def load_merkelypipe(file):
    return json.load(file)


import subprocess
def sha_digest_for_file(artifact_path):
    output = subprocess.check_output(["openssl", "dgst", "-sha256", artifact_path])
    digest_in_bytes = output.split()[1]
    artifact_sha = digest_in_bytes.decode('utf-8')
    return artifact_sha


def create_artifact(api_token, host, merkelypipe,
                    sha256, filename,
                    description, git_commit, commit_url, build_url):
    create_artifact_payload = {
        "sha256": sha256,
        "filename": filename,
        "description": description,
        "git_commit": git_commit,
        "commit_url": commit_url,
        "build_url": build_url
        #"is_compliant": is_compliant
    }
    url = ApiSchema.url_for_artifacts(host, merkelypipe)
    http_put_payload(url, create_artifact_payload, api_token)
