from commands import *

COMMANDS = {
    "declare_pipeline": DeclarePipeline,
    "log_artifact": LogArtifact,
    "log_deployment": LogDeployment,
    "log_evidence": LogEvidence,
    "log_approval": LogApproval,
    "log_test": LogTest,
    "control_deployment": ControlDeployment,
    "control_pull_request": ControlPullRequest,
}
