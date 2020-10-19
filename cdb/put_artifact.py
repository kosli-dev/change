#!/usr/bin/env python

from cdb.cdb_utils import parse_cmd_line, put_artifact


def main():
    project_file = parse_cmd_line()
    put_artifact(project_file)


if __name__ == '__main__':
    main()
