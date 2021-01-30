from cdb.api_schema import ApiSchema
from cdb.http import http_put_payload


def execute(context):
    env = context['env']
    command = env.get("MERKELY_COMMAND", None)
    print("MERKELY_COMMAND={}".format(command))
    merkleypipe_path = "/Merkelypipe.json"
    with open(merkleypipe_path) as merkelypipe_file:
        merkelypipe = load_merkelypipe(merkelypipe_file)
        api_token = env.get('MERKELY_API_TOKEN', None)
        host = "https://app.compliancedb.com"
        if command == "declare_pipeline":
            declare_pipeline(context, merkelypipe, api_token, host)
        if command == "log_artifact":
            log_artifact(context, merkelypipe, api_token, host)

    return 0


def declare_pipeline(_context, merkelypipe, api_token, host):
    pipelines_url = ApiSchema.url_for_pipelines(host, merkelypipe)
    http_put_payload(url=pipelines_url, payload=merkelypipe, api_token=api_token)


def log_artifact(context, merkelypipe, api_token, host):
    env = context['env']
    fingerprint = env.get("MERKELY_FINGERPRINT", None)

    context['description'] = "Created by build " + env.get('MERKELY_CI_BUILD_NUMBER', None)
    context['git_commit'] = env.get('MERKELY_ARTIFACT_GIT_COMMIT', None)
    context['commit_url'] = env.get('MERKELY_ARTIFACT_GIT_URL', None)
    context['build_url'] = env.get('MERKELY_CI_BUILD_URL', None)

    if fingerprint.startswith("file://"):
        context['artifact_name'] = fingerprint[len("file://"):]
        log_artifact_file(context, merkelypipe, api_token, host)
    if fingerprint.startswith("docker://"):
        context['artifact_name'] = fingerprint[len("docker://"):]
        log_artifact_docker_image(context, merkelypipe, api_token, host)


def log_artifact_file(context, merkelypipe, api_token, host):
    pathed_filename = '/' + context['artifact_name']
    print("Getting SHA for artifact: " + pathed_filename)  # print "file://" ?
    artifact_sha = context['sha_digest_for_file'](pathed_filename)
    print("Calculated digest: " + artifact_sha)
    #print("Publish artifact to ComplianceDB")

    # is_compliant = env_is_compliant()
    # print('CDB_IS_COMPLIANT: ' + str(is_compliant))
    create_artifact(api_token, host, merkelypipe,
                    artifact_sha, pathed_filename,
                    context['description'],
                    context['git_commit'],
                    context['commit_url'],
                    context['build_url'])


def log_artifact_docker_image(context, merkelypipe, api_token, host):
    image_name = context['artifact_name']
    print("Getting SHA for artifact: " + image_name)  # print "docker://" ?
    artifact_sha = context['sha_digest_for_docker_image'](image_name)
    print("Calculated digest: " + artifact_sha)
    #print("Publish artifact to ComplianceDB")

    # is_compliant = env_is_compliant()
    # print('CDB_IS_COMPLIANT: ' + str(is_compliant))
    create_artifact(api_token, host, merkelypipe,
                    artifact_sha, image_name,
                    context['description'],
                    context['git_commit'],
                    context['commit_url'],
                    context['build_url'])


import json
def load_merkelypipe(file):
    return json.load(file)


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
