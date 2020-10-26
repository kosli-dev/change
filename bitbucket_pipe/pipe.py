import os
import sys
from bitbucket_pipes_toolkit import Pipe, get_logger

from cdb.bitbucket import get_bitbucket_repo_url

sys.path.append('/app/')
import cdb.cdb_utils
import cdb.bitbucket
from cdb.cdb_utils import set_artifact_sha_env_variable_from_file_or_image


schema = {
    'CDB_COMMAND': {'type': 'string', 'required': True},
    'CDB_PIPELINE_DEFINITION': {'type': 'string', 'required': True},
    'CDB_API_TOKEN': {'type': 'string', 'required': True},
    # PUT Pipeline Variables
    #   ...none...
    # Put Artifact Variables
    'CDB_IS_COMPLIANT': {'type': 'boolean', 'required': False},
    'CDB_ARTIFACT_GIT_URL': {'type': 'string', 'required': False},
    'CDB_ARTIFACT_GIT_COMMIT': {'type': 'string', 'required': False},
    'CDB_CI_BUILD_URL': {'type': 'string', 'required': False},
    'CDB_BUILD_NUMBER': {'type': 'string', 'required': False},
    'CDB_ARTIFACT_SHA': {'type': 'string', 'required': False},
    'CDB_ARTIFACT_FILENAME': {'type': 'string', 'required': False},

}

logger = get_logger()


class DemoPipe(Pipe):
    def run(self):
        super().run()

        logger.info('Executing the pipe...')

        command = self.get_variable('CDB_COMMAND')
        pipeline_definition_file = self.get_variable('CDB_PIPELINE_DEFINITION')
        api_token = self.get_variable('CDB_API_TOKEN')

        print("Command: " + command)
        print("Pipeline: " + pipeline_definition_file)
        print("API_TOKEN: " + api_token)

        if command == "put_pipeline":
            cdb.cdb_utils.put_pipeline(pipeline_definition_file)
        if command == "put_artifact":
            self.adapt_put_artifact_env_variables()
            cdb.cdb_utils.put_artifact(pipeline_definition_file)
        if command == "put_artifact_image":
            self.adapt_put_artifact_image_env_variables()
            cdb.cdb_utils.put_artifact_image(pipeline_definition_file)
        if command == "control_junit":
            self.adapt_control_junit_env_variables()
            cdb.cdb_utils.control_junit(pipeline_definition_file)
        if command == "control_bitbucket_pr":
            set_artifact_sha_env_variable_from_file_or_image()
            cdb.bitbucket.put_bitbucket_pull_request(pipeline_definition_file)
        if command == "create_release":
            self.adapt_create_release_variables()
            cdb.cdb_utils.create_release(pipeline_definition_file)

        self.success(message="Success!")

    def adapt_put_artifact_image_env_variables(self):
        self.adapt_bitbucket_env_variables()
        set_artifact_sha_env_variable_from_file_or_image()

    @staticmethod
    def adapt_create_release_variables():
        DemoPipe.adapt_bitbucket_env_variables()
        set_artifact_sha_env_variable_from_file_or_image()
        os.environ["CDB_SRC_REPO_ROOT"] = os.environ.get("BITBUCKET_CLONE_DIR") + "/"

    @staticmethod
    def adapt_control_junit_env_variables():
        DemoPipe.adapt_bitbucket_env_variables()
        set_artifact_sha_env_variable_from_file_or_image()

    @staticmethod
    def adapt_put_artifact_env_variables():
        DemoPipe.adapt_bitbucket_env_variables()
        set_artifact_sha_env_variable_from_file_or_image()

    @staticmethod
    def adapt_bitbucket_env_variables():
        repo_url = get_bitbucket_repo_url()

        bb_commit = os.environ.get("BITBUCKET_COMMIT")
        bb_build_number = os.environ.get("BITBUCKET_BUILD_NUMBER")

        build_url = f"{repo_url}/addon/pipelines/home#!/results/{bb_build_number}"

        os.environ["CDB_ARTIFACT_GIT_URL"] = f"{repo_url}/commits/{bb_commit}"
        os.environ["CDB_ARTIFACT_GIT_COMMIT"] = bb_commit
        os.environ["CDB_BUILD_NUMBER"] = bb_build_number
        os.environ["CDB_CI_BUILD_URL"] = build_url


if __name__ == '__main__':
    pipe = DemoPipe(pipe_metadata='/pipe.yml', schema=schema)
    pipe.run()
