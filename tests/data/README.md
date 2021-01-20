# About this test data

The file `test_source_repo.tar.gz` contains a small git repository for 
testing our git graph parsing logic.
It becomes part of the Docker image thanks to the Dockerfile command:

    `ADD tests/data/test_source_repo.tar.gz /`

which untars the file into the / dir, thus creating the '/test_src' dir
which contains a `.git` dir.

The tests are under [tests/unit/test_git.py](../unit/test_git.py)
