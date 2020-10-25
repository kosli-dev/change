from cdb.bitbucket import put_bitbucket_pull_request
from cdb.cdb_utils import parse_cmd_line

if __name__ == '__main__':
    project_config_file = parse_cmd_line()
    put_bitbucket_pull_request(project_config_file)