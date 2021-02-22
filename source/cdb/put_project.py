#!/usr/bin/env python
from cdb.cdb_utils import parse_cmd_line
from cdb.put_pipeline import put_pipeline


def main():
    """
    project.json
    """
    project_file = parse_cmd_line()
    put_pipeline(project_file)


if __name__ == '__main__':
    main()
