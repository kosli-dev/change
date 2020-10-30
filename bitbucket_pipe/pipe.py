import sys
from bitbucket_pipes_toolkit import Pipe, get_logger

import cdb.control_junit
import cdb.create_release
import cdb.put_artifact
import cdb.put_artifact_image
import cdb.put_pipeline
from cdb.bitbucket import get_bitbucket_repo_url, adapt_put_artifact_image_env_variables, \
    adapt_create_release_variables, adapt_control_junit_env_variables, adapt_put_artifact_env_variables

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


class BitbucketPipe(Pipe):
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
            cdb.put_pipeline.put_pipeline(pipeline_definition_file)
        if command == "put_artifact":
            adapt_put_artifact_env_variables()
            cdb.put_artifact.put_artifact(pipeline_definition_file)
        if command == "put_artifact_image":
            adapt_put_artifact_image_env_variables()
            cdb.put_artifact_image.put_artifact_image(pipeline_definition_file)
        if command == "control_junit":
            adapt_control_junit_env_variables()
            cdb.control_junit.control_junit(pipeline_definition_file)
        if command == "control_bitbucket_pr":
            set_artifact_sha_env_variable_from_file_or_image()
            cdb.bitbucket.put_bitbucket_pull_request(pipeline_definition_file)
        if command == "create_release":
            adapt_create_release_variables()
            cdb.create_release.create_release(pipeline_definition_file)

        self.success(message="Success!")


if __name__ == '__main__':
    pipe = BitbucketPipe(pipe_metadata='/pipe.yml', schema=schema)
    pipe.run()
