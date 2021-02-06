from commands import *


def execute(context):
    try:
        cmd = make_command(context)
        if cmd is not None:
            print(f"MERKELY_COMMAND={cmd.name.value}")
            for env_var in list(cmd.env_vars):
                env_var.verify()
            return cmd.execute()
    except CommandError as exc:
        print(f"Error: {str(exc)}")
        return 144


def make_command(context):
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
