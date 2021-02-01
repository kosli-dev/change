from commands import CommandError
from commands import DeclarePipelineCommand
from commands import LogArtifactCommand


def execute(context):
    try:
        command = get_command(context)
        if command == "declare_pipeline":
            DeclarePipelineCommand(context).execute()
        if command == "log_artifact":
            LogArtifactCommand(context).execute()
        return 0
    except CommandError as exc:
        print(f"ERROR: {str(exc)}")
        return exc.status_code


def get_command(context):
    command = context.env.get("MERKELY_COMMAND", None)
    if command is None:
        raise CommandError(23, "MERKELY_COMMAND environment-variable not set")
    if command == "":
        raise CommandError(24, "MERKELY_COMMAND environment-variable is empty string")
    return command
