from cdb.api_schema import ApiSchema
from cdb.http import http_put_payload


def execute(context):
    def env(name):
        return get_env(context, name)
    command = env("MERKELY_COMMAND")
    print("MERKELY_COMMAND={}".format(command))
    MERKELYPIPE_PATH = "/Merkelypipe.json"
    with open(MERKELYPIPE_PATH) as file:
        merkelypipe = load_merkelypipe(file)
        api_token = env('MERKELY_API_TOKEN')
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
    def env(name):
        return get_env(context, name)

    fingerprint = env("MERKELY_FINGERPRINT")

    context['description'] = "Created by build " + env('MERKELY_CI_BUILD_NUMBER')
    context['git_commit'] = env('MERKELY_ARTIFACT_GIT_COMMIT')
    context['commit_url'] = env('MERKELY_ARTIFACT_GIT_URL')
    context['build_url'] = env('MERKELY_CI_BUILD_URL')

    FILE_PROTOCOL = "file://"
    DOCKER_PROTOCOL = "docker://"

    if fingerprint.startswith(FILE_PROTOCOL):
        context['artifact_name'] = fingerprint[len(FILE_PROTOCOL):]
        log_artifact_file(context, merkelypipe, api_token, host)

    if fingerprint.startswith(DOCKER_PROTOCOL):
        context['artifact_name'] = fingerprint[len(DOCKER_PROTOCOL):]
        log_artifact_docker_image(context, merkelypipe, api_token, host)


def log_artifact_file(context, merkelypipe, api_token, host):
    pathed_filename = '/' + context['artifact_name']
    print("Getting SHA for file:// artifact: " + pathed_filename)
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
    print("Getting SHA for docker:// artifact: " + image_name)
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


def get_env(context, name):
    return context['env'].get(name, None)


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
