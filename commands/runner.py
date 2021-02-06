from os import environ
from commands import Context, Fingerprinter, build_command, CommandError


def run(env=None, fingerprinter=None):
    if env is None:
        env = environ
    if fingerprinter is None:
        fingerprinter = Fingerprinter()
    try:
        context = Context(env, fingerprinter)
        command = build_command(context)
        print(f"MERKELY_COMMAND={command.name.value}")
        for env_var in list(command.env_vars):
            env_var.verify()
        return command()
    except CommandError as exc:
        print(f"Error: {str(exc)}")
        return 144


