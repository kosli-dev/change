import os
import subprocess
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
            self.adapt_bitbucket_env_variables()
            cdb.cdb_utils.put_artifact_image(pipeline_definition_file)
        if command == "control_junit":
            self.adapt_control_junit_env_variables()
            cdb.cdb_utils.control_junit(pipeline_definition_file)
        if command == "create_release":
            self.adapt_create_release_variables()
            cdb.cdb_utils.create_release(pipeline_definition_file)

        self.success(message="Success!")

    @staticmethod
    def adapt_create_release_variables():
        DemoPipe.adapt_bitbucket_env_variables()
        DemoPipe.compute_artifact_sha()
        os.environ["CDB_SRC_REPO_ROOT"] = os.environ.get("BITBUCKET_CLONE_DIR") + "/"

    @staticmethod
    def adapt_control_junit_env_variables():
        DemoPipe.adapt_bitbucket_env_variables()
        DemoPipe.compute_artifact_sha()

    @staticmethod
    def adapt_put_artifact_env_variables():
        DemoPipe.adapt_bitbucket_env_variables()
        DemoPipe.compute_artifact_sha()

    @staticmethod
    def compute_artifact_sha():
        artifact_filename = os.environ.get("CDB_ARTIFACT_FILENAME", None)
        artifact_docker_image = os.environ.get("CDB_ARTIFACT_DOCKER_IMAGE", None)

        if artifact_filename is not None:
            print("Getting SHA for artifact: " + artifact_filename)
            artifact_sha = DemoPipe.calculate_sha_digest(artifact_filename)
            print("Calculated digest: " + artifact_sha)
            os.environ["CDB_ARTIFACT_SHA"] = artifact_sha
        elif artifact_docker_image is not None:
            print("Getting SHA for docker image: " + artifact_filename)
            artifact_sha = DemoPipe.calculate_sha_digest(artifact_docker_image)
            print("Calculated digest: " + artifact_sha)
            os.environ["CDB_ARTIFACT_SHA"] = artifact_sha
        else:
            raise Exception('Error: CDB_ARTIFACT_FILENAME or CDB_ARTIFACT_DOCKER_IMAGE must be defined')


    @staticmethod
    def adapt_bitbucket_env_variables():
        bb_repo_slug = os.environ.get("BITBUCKET_REPO_SLUG")
        bb_commit = os.environ.get("BITBUCKET_COMMIT")
        bb_build_number = os.environ.get("BITBUCKET_BUILD_NUMBER")
        bb_workspace = os.environ.get("BITBUCKET_WORKSPACE")

        repo_url = f"https://bitbucket.org/{bb_workspace}/{bb_repo_slug}"
        build_url = f"{repo_url}/addon/pipelines/home#!/results/{bb_build_number}"

        os.environ["CDB_ARTIFACT_GIT_URL"] = f"{repo_url}/commits/{bb_commit}"
        os.environ["CDB_ARTIFACT_GIT_COMMIT"] = bb_commit
        os.environ["CDB_BUILD_NUMBER"] = bb_build_number
        os.environ["CDB_CI_BUILD_URL"] = build_url

    @staticmethod
    def calculate_sha_digest(artifact_filename):
        if not os.path.isfile(artifact_filename):
            raise FileNotFoundError
        output = subprocess.check_output(["openssl", "dgst", "-sha256", artifact_filename])
        digest_in_bytes = output.split()[1]
        artifact_sha = digest_in_bytes.decode('utf-8')
        return artifact_sha


if __name__ == '__main__':
    pipe = DemoPipe(pipe_metadata='/pipe.yml', schema=schema)
    pipe.run()
