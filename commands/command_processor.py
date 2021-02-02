from commands import Command
from commands import DeclarePipelineCommand
from commands import LogArtifactCommand


def execute(context):
    try:
        command = None
        name = Command(context).name
        if name == "declare_pipeline":
            command = DeclarePipelineCommand
        if name == "log_artifact":
            command = LogArtifactCommand

        if command is not None:
            command(context).execute()
        return 0
    except Command.Error as exc:
        print(f"ERROR: {str(exc)}")
        return 144
