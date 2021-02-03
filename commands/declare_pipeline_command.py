from commands import Command
from cdb.api_schema import ApiSchema
from cdb.http import http_put_payload


class DeclarePipelineCommand(Command):
    """
    Declares a pipeline in Merkely. Invoked like this:

    docker run \
            --env MERKELY_COMMAND=declare_pipeline \
            \
            --env MERKELY_API_TOKEN=${YOUR_API_TOKEN} \
            --env MERKELY_HOST=https://app.merkely.com \
            --rm \
            --volume ${YOUR_MERKELY_PIPE}:/Merkelypipe.json \
            merkely/change
    """
    @property
    def args(self):
        return (self.api_token,
                self.host)

    def _verify_args(self):
        for arg in self.args:
            arg.verify()

    @property
    def api_token(self):
        return self._required_env_var("API_TOKEN")

    @property
    def host(self):
        return self._required_env_var("HOST")

    def _concrete_execute(self):
        pipelines_url = ApiSchema.url_for_pipelines(self.host.value, self.merkelypipe)
        http_put_payload(url=pipelines_url, payload=self.merkelypipe, api_token=self.api_token.value)
