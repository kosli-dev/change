#!/usr/bin/env python

from cdb.cdb_utils import create_release, parse_cmd_line

if __name__ == '__main__':
    project_config_file = parse_cmd_line()
    create_release(project_config_file)
