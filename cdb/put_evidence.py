#!/usr/bin/env python

from cdb.cdb_utils import put_evidence, parse_cmd_line

if __name__ == '__main__':
    project_file = parse_cmd_line()
    put_evidence(project_file)
