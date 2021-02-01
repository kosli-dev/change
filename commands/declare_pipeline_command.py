from commands import Command
from cdb.api_schema import ApiSchema
from cdb.http import http_put_payload


class DeclarePipelineCommand(Command):
    """
    Command subclass for handling MERKELY_COMMAND=declare_pipeline
    """
    def _concrete_execute(self):
        pipelines_url = ApiSchema.url_for_pipelines(self.host, self.merkelypipe)
        http_put_payload(url=pipelines_url, payload=self.merkelypipe, api_token=self.api_token)
