#!/usr/bin/env python

from cdb.cdb_utils import parse_cmd_line, put_artifact_image


def main():
    project_file = parse_cmd_line()
    put_artifact_image(project_file)


if __name__ == '__main__':
    main()
