#!/usr/bin/env python
from cdb.cdb_utils import put_pipeline, parse_cmd_line


def main():
    """
    project.json
    """
    project_file = parse_cmd_line()
    put_pipeline(project_file)


if __name__ == '__main__':
    main()
