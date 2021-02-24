from commands import *


def test_invocation_strings():
    command_klasses = [
        DeclarePipeline,
        ControlDeployment,
        LogApproval,
        LogArtifact,
        LogDeployment,
        LogEvidence,
        LogTest,
    ]
    for klass in command_klasses:
        context = External(new_log_approval_env())
        command = klass(context)
        assert len(command.invocation('full')) > 0
        assert len(command.invocation('minimum')) > 0


CDB_DOMAIN = "app.compliancedb.com"
API_TOKEN = "5199831f4ee3b79e7c5b7e0ebe75d67aa66e79d4"


def new_log_approval_env():
    protocol = "docker://"
    image_name = "acme/runner:4.56"
    domain = CDB_DOMAIN
    return {
        "MERKELY_COMMAND": "log_approval",
        "MERKELY_FINGERPRINT": f"{protocol}{image_name}",
        "MERKELY_API_TOKEN": API_TOKEN,
        "MERKELY_HOST": f"https://{domain}",
        "MERKELY_NEWEST_SRC_COMMITISH": "master",
        "MERKELY_OLDEST_SRC_COMMITISH": "production",
        "MERKELY_DESCRIPTION": "No description provided"
    }