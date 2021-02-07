from os import environ
from commands import Context, build_command, CommandError
from commands import DockerFingerprinter, FileFingerprinter


def run(env=None, docker_fingerprinter=None, file_fingerprinter=None):
    if env is None:
        env = environ
    if docker_fingerprinter is None:
        docker_fingerprinter = DockerFingerprinter()
    if file_fingerprinter is None:
        file_fingerprinter = FileFingerprinter()
    try:
        context = Context(env, docker_fingerprinter, file_fingerprinter)
        command = build_command(context)
        print(f"MERKELY_COMMAND={command.name.value}")
        for env_var in list(command.env_vars):
            env_var.value  # to verify
        return command()
    except CommandError as exc:
        print(f"Error: {str(exc)}")
        return 144


