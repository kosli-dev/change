from commands import Command
from commands import DeclarePipelineCommand
from commands import LogArtifactCommand


def execute(context):
    try:
        command = Command(context).name
        if command == "declare_pipeline":
            DeclarePipelineCommand(context).execute()
        if command == "log_artifact":
            LogArtifactCommand(context).execute()
        return 0
    except Command.Error as exc:
        print(f"ERROR: {str(exc)}")
        return exc.status_code
