from commands import *


def execute(context):
    try:
        cmd = make_command(context)
        if cmd is not None:
            print(f"MERKELY_COMMAND={cmd.name.value}")
            cmd.verify_args()
            return cmd.execute()
    except CommandError as exc:
        print(f"ERROR: {str(exc)}")
        return 144


def make_command(context):
    name = Command(context).name.value
    if name == "declare_pipeline":
        return DeclarePipelineCommand(context)
    if name == "log_artifact":
        return LogArtifactCommand(context)
    if name == "log_deployment":
        return LogDeploymentCommand(context)
    return None
