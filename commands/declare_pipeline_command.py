from commands import Command
from cdb.api_schema import ApiSchema
from cdb.http import http_put_payload


class DeclarePipelineCommand(Command):
    """
    Declares a pipeline in Merkely.
    Invoked like this:

    docker run \
        --env MERKELY_COMMAND=declare_pipeline \
        --env MERKELY_API_TOKEN=${YOUR_API_TOKEN} \
        --rm \
        --volume ${YOUR_MERKELY_PIPE}:/Merkelypipe.json \
        merkely/change
    """

    def __call__(self):
        url = ApiSchema.url_for_pipelines(self.host.value, self.merkelypipe)
        payload = self.merkelypipe
        http_put_payload(url, payload, api_token=self.api_token.value)
        return 'Putting', url, payload

    @property
    def _env_var_names(self):
        return [
            'api_token',
            'host',
            'name',
        ]
