import os
import sys
sys.path.append(os.path.abspath("/app/source"))
from commands import Command
from docs import doc_ref

CI_NAMES = [ 'docker', 'github', 'bitbucket' ]


def test_ref_targets():
    doc_ref.curl_ref_files()
    command_names = Command.names()
    for command_name in command_names:
        command = Command.named(command_name)({})
        for ci_name in CI_NAMES:
            ref = command.doc_ref(ci_name)
            assert isinstance(ref, str), command_name + ':' + ci_name


