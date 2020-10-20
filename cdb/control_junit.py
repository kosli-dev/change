#!/usr/bin/env python

from cdb.cdb_utils import control_junit, parse_cmd_line

if __name__ == '__main__':
    project_file = parse_cmd_line()
    control_junit(project_file)
