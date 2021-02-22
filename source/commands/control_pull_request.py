from errors import ChangeError
from commands import Command
from cdb.api_schema import ApiSchema
from cdb.http import http_put_payload


class ControlPullRequest(Command):

    @property
    def summary(self):
        return ""

    def invocation(self, _type):
        return ""

    def __call__(self):
        payload = {
            #...
        }
        url = ApiSchema.url_for_artifact(self.host.value, self.merkelypipe, self.fingerprint.sha256)
        http_put_payload(url, payload, self.api_token.value)
        return 'Putting', url, payload

    @property
    def description(self):
        notes = f"A description for the pull request."
        return self._required_env_var("MERKELY_DESCRIPTION", notes)

    @property
    def _env_var_names(self):
        # Print according to this order
        return [
            'name',
            'fingerprint',
            #...
            'description',
            'is_compliant',
            'api_token',
            'host',
        ]
