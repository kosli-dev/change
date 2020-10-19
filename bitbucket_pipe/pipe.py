
import sys
from bitbucket_pipes_toolkit import Pipe, get_logger

sys.path.append('/app/')
import cdb.cdb_utils


schema = {
    'CDB_COMMAND': {'type': 'string', 'required': True},
    'CDB_PIPELINE_DEFINITION': {'type': 'string', 'required': True},
    'CDB_API_TOKEN': {'type': 'string', 'required': True},
    # PUT Pipeline Variables
    #   ...none...
    # Put Artifact Variables
    'CDB_IS_COMPLIANT': {'type': 'string', 'required': False},
    'CDB_ARTIFACT_GIT_URL': {'type': 'string', 'required': False},
    'CDB_ARTIFACT_GIT_COMMIT': {'type': 'string', 'required': False},
    'CDB_CI_BUILD_URL': {'type': 'string', 'required': False},
    'CDB_BUILD_NUMBER': {'type': 'string', 'required': False},
    'CDB_ARTIFACT_SHA': {'type': 'string', 'required': False},
    'CDB_ARTIFACT_FILENAME': {'type': 'string', 'required': False},

}
"""



export CDB_ARTIFACT_GIT_URL=https://bitbucket.org/ztlpay/${BITBUCKET_REPO_SLUG}/commits/${BITBUCKET_COMMIT}
export CDB_ARTIFACT_GIT_COMMIT=${BITBUCKET_COMMIT}
CDB_CI_BUILD_URL="https://bitbucket.org/ztlpay/${BITBUCKET_REPO_SLUG}/addon/pipelines"
CDB_CI_BUILD_URL+='/home#!/results/'
CDB_CI_BUILD_URL+=${BITBUCKET_BUILD_NUMBER}
export CDB_CI_BUILD_URL
export CDB_BUILD_NUMBER=${BITBUCKET_BUILD_NUMBER}
export CDB_DOCKER_IMAGE=$IMAGE_NAME


            --env CDB_IS_COMPLIANT=${CDB_IS_COMPLIANT} \
            --env CDB_ARTIFACT_GIT_URL=${CDB_ARTIFACT_GIT_URL} \
            --env CDB_ARTIFACT_GIT_COMMIT=${CDB_ARTIFACT_GIT_COMMIT} \
            --env CDB_CI_BUILD_URL=${CDB_CI_BUILD_URL} \
            --env CDB_BUILD_NUMBER=${CDB_BUILD_NUMBER} \
            --env CDB_ARTIFACT_SHA=$DIGEST \
            --env CDB_ARTIFACT_FILENAME=${IMAGE_NAME} \
"""

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

        cdb.cdb_utils.hello_world()
        if command == "put_pipeline":
            cdb.cdb_utils.put_pipeline(pipeline_definition_file)
        self.success(message="Success!")


if __name__ == '__main__':
    pipe = DemoPipe(pipe_metadata='/pipe.yml', schema=schema)
    pipe.run()
