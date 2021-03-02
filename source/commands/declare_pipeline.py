from commands import Command
from cdb.api_schema import ApiSchema
from cdb.http import http_put_payload


class DeclarePipeline(Command):

    def summary(self, _ci):
        return "Declares a pipeline in Merkely"

    def ci_yml(self, ci):
        if ci != 'github':
            return 0, ""
        if ci == 'github':
            return 8, "\n".join([
                "jobs:",
                "  build:",
                "    runs-on: ubuntu-latest",
                "",
                "    steps:",
                "    - uses: actions/checkout@v2",
                "",
                "    - name: Declare Merkely pipeline",
                "      env:",
                "        MERKELY_API_TOKEN: ${{secrets.MERKELY_API_TOKEN}}",
                "      run: |",
                "",
            ])

    @property
    def volume_mounts(self):
        return []

    def __call__(self):
        url = ApiSchema.url_for_pipelines(self.host.value, self.merkelypipe)
        payload = self.merkelypipe
        http_put_payload(url, payload, self.api_token.value)
        return 'Putting', url, payload

    @property
    def _merkely_env_var_names(self):
        return [
            'name',
            'api_token',
            'host',
        ]
