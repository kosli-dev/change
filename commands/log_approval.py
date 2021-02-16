from commands import Command
from cdb.api_schema import ApiSchema
from cdb.http import http_post_payload
from cdb.git import list_commits_between
from pygit2 import Repository, _pygit2


class LogApproval(Command):

    @property
    def summary(self):
        return ""

    def invocation(self, type):
        def env(var):
            if var.name == "MERKELY_COMMAND":
                value = var.value
            elif var.name == "MERKELY_FINGERPRINT":
                value = var.example
            else:
                value = "${...}"
            return f'    --env {var.name}="{value}" \\\n'

        invocation_string = "docker run \\\n"
        for name in self._env_var_names:
            var = getattr(self, name)
            if type == 'full':
                invocation_string += env(var)
            if type == 'minimum' and var.is_required:
                invocation_string += env(var)

        invocation_string += "    --rm \\\n"
        invocation_string += "    --volume ${PWD}:/src \\\n"
        invocation_string += "    --volume /var/run/docker.sock:/var/run/docker.sock \\\n"
        invocation_string += "    --volume ${YOUR_MERKELY_PIPE}:/Merkelypipe.json \\\n"
        invocation_string += "    merkely/change"
        return invocation_string

    def __call__(self):
        commit_list = list_commits_between(repo_at(self.src_repo_root.value),
                                           self.target_src_commitish.value,
                                           self.base_src_commitish.value)
        payload = {
            "artifact_sha256": self.fingerprint.sha,
            "description": self.description.value,
            "is_approved": self.is_approved.value == 'TRUE',
            "src_commit_list": commit_list,
        }
        url = ApiSchema.url_for_approvals(self.host.value, self.merkelypipe)
        http_post_payload(url, payload, self.api_token.value)
        return 'Posting', url, payload

    @property
    def description(self):
        notes = f"A description for the approval."
        return self._required_env_var("DESCRIPTION", notes)

    @property
    def target_src_commitish(self):
        notes = "The source commit-ish for the oldest change in the approval."
        return self._required_env_var("TARGET_SRC_COMMITISH", notes)

    @property
    def base_src_commitish(self):
        notes = "The source commit-ish for the newest change in the approval."
        return self._required_env_var("BASE_SRC_COMMITISH", notes)

    @property
    def src_repo_root(self):
        default = "/src"
        notes = " ".join([
            "The directory where the source git repository is volume-mounted.",
            f"Defaults to `{default}`",
            ''
         ])
        return self._static_defaulted_env_var("SRC_REPO_ROOT", default, notes)

    @property
    def is_approved(self):
        default = 'TRUE'
        notes = f"Defaults to {default}"
        return self._static_defaulted_env_var("IS_APPROVED", default, notes)

    @property
    def _env_var_names(self):
        # Print according to this order
        return [
            'name',
            'fingerprint',
            'target_src_commitish',
            'base_src_commitish',
            'description',
            'is_approved',
            'src_repo_root',
            'api_token',
            'host',
        ]


def repo_at(root):
    try:
        repo = Repository(root + '/.git')
    except _pygit2.GitError as err:
        print("Error: " + str(err))
        return None
    return repo