from commands import Command
from env_vars import *
#from cdb.api_schema import ApiSchema
#from cdb.http import http_put_payload


class LogApprovalCommand(Command):

    def __call__(self):
        pass

    @property
    def release_description(self):
        return DescriptionEnvVar(self.env)

    @property
    def evidence_type(self):
        notes = "The evidence type."
        return self._required_env_var("EVIDENCE_TYPE", notes)

    @property
    def _env_var_names(self):
        # Print according to this order
        return [
            'name',
            'fingerprint',
            'target_src_commitish',
            'base_src_commitish',
            'release_description',
            'src_repo_root',
            'evidence_type',
            'api_token',
            'host',
        ]

        # "MERKELY_TARGET_SRC_COMMITISH": "todo",
        # "MERKELY_BASE_SRC_COMMITISH": "todo",
        # "MERKELY_RELEASE_DESCRIPTION": "todo",
        # "MERKELY_SRC_REPO_ROOT": "todo",  DEFAULT_REPO_ROOT
        # "MERKELY_EVIDENCE_TYPE": "unit_test",
        # "MERKELY_RELEASE_DESCRIPTION": "branch coverage"
