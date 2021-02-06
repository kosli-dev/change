from commands import *


def build_command(context):
    name = Command(context).name.value
    if name == "declare_pipeline":
        return DeclarePipelineCommand(context)
    if name == "log_artifact":
        return LogArtifactCommand(context)
    if name == "log_deployment":
        return LogDeploymentCommand(context)
    if name == "log_evidence":
        return LogEvidenceCommand(context)
    return None
