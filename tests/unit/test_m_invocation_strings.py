from commands import *


def test_invocation_strings():
    command_klasses = [
        DeclarePipeline,
        LogApproval,
        LogArtifact,
        LogDeployment,
        LogEvidence,
        LogTest,
        ControlDeployment,
        ControlPullRequest
    ]
    for klass in command_klasses:
        env = {"MERKELY_COMMAND": "unused"}
        external = External(env=env)
        assert len(klass(external).invocation('full')) > 0
        assert len(klass(external).invocation('minimum')) > 0


