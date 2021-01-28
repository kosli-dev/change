from cdb.api_schema import ApiSchema
from cdb.cdb_utils import load_project_configuration
from cdb.http import http_put_payload


def load_merkelypipe(file):
    return load_project_configuration(file)


def execute(env):
    print("MERKELY_COMMAND=declare_pipeline")
    merkleypipe_path = "/Merkelypipe.json"
    with open(merkleypipe_path) as merkelypipe_file:
        merkelypipe_data = load_merkelypipe(merkelypipe_file)
        host = "https://app.compliancedb.com"
        pipelines_url = ApiSchema.url_for_pipelines(host, merkelypipe_data)
        api_token = env.get('MERKELY_API_TOKEN', None)
        http_put_payload(url=pipelines_url, payload=merkelypipe_data, api_token=api_token)

    return 0
