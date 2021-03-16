from source import *


def test_generate_docs():
    docs = generate_docs()
    assert "/docs/build/reference/github/log_test.txt" in docs.keys()


def test_lines_for_command_reference_string():
    lines_for('bitbucket', 'log_test')
    lines_for('docker', 'log_test')
    lines_for('github', 'log_test')


def test_lines_for_minimum_use_string():
    min_lines_for('log_test')


