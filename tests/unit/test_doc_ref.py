import os
import sys
sys.path.append(os.path.abspath("/app/source"))
from docs import REF_FILES
from .doc_ref_cache import read_doc_ref_cache
from commands import Command

CI_NAMES = ['docker', 'github', 'bitbucket']


def test_ref_targets():
    global REF_FILES
    REF_FILES.update(read_doc_ref_cache())
    command_names = Command.names()
    for command_name in command_names:
        command = Command.named(command_name)({})
        ref = command.doc_ref()
        assert type(ref) is dict, command_name
