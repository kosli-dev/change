# Merkely Pipeline Controls

![Continuous Integration Status](https://github.com/merkely-development/change/workflows/CI/badge.svg)

This docker image provides some helpers for gathering the audit trail and performing controls in your devops pipelines.

    docker pull merkely/change
    
To learn more about DevOps Change Management, and how to use this image see the [documentation site](https://docs.merkely.com)

- Test the application:
    ```shell
    make test_unit 
    ```
    The following bash function runs only unit tests whose name is a grep match for ${1}:
    ```shell
    mtuk() { make test_unit        TARGET="-k ${1}"; }
    ```