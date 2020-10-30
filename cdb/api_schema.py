class ApiSchema:
    @staticmethod
    def url_for_owner_projects(host, project_data):
        return host + '/api/v1/projects/' + project_data["owner"] + "/"

    @staticmethod
    def url_for_project(host, project_data):
        return ApiSchema.url_for_owner_projects(host, project_data) + project_data["name"]

    @staticmethod
    def url_for_releases(host, project_data):
        return ApiSchema.url_for_project(host, project_data) + '/releases/'

    @staticmethod
    def url_for_commit(host, project_data, commit):
        return ApiSchema.url_for_project(host, project_data) + '/commits/' + commit

    @staticmethod
    def url_for_artifacts(host, project_data):
        return ApiSchema.url_for_project(host, project_data) + '/artifacts/'

    @staticmethod
    def url_for_artifact(host, project_data, sha256_digest):
        return ApiSchema.url_for_artifacts(host, project_data) + sha256_digest

    @staticmethod
    def url_for_artifacts(host, project_data):
        return ApiSchema.url_for_project(host, project_data) + '/artifacts/'

    @staticmethod
    def url_for_release(host, project_data, release_number):
        return ApiSchema.url_for_releases(host, project_data) + release_number