from commands import DeclarePipelineCommand
from commands import LogArtifactCommand


def execute(context):
    command = context.env.get("MERKELY_COMMAND", None)
    if command == "declare_pipeline":
        DeclarePipelineCommand(context).execute()
    if command == "log_artifact":
        LogArtifactCommand(context).execute()
    return 0


