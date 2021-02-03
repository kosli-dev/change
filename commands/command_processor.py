from commands import Command, CommandError, DeclarePipelineCommand, LogArtifactCommand


def execute(context):
    try:
        cls = None
        name = Command(context).name
        if name == "declare_pipeline":
            cls = DeclarePipelineCommand
        if name == "log_artifact":
            cls = LogArtifactCommand

        if cls is not None:
            print(f"MERKELY_COMMAND={name}")
            command = cls(context)
            for arg in command.args:
                arg.verify()
            command.execute()
        return 0
    except CommandError as exc:
        print(f"ERROR: {str(exc)}")
        return 144
