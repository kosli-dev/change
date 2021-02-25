from errors import ChangeError
from commands import build_command, External


def run(*, env=None, docker_fingerprinter=None, file_fingerprinter=None):
    context = External(env=env,
                       docker_fingerprinter=docker_fingerprinter,
                       file_fingerprinter=file_fingerprinter)
    name = context.env.get("MERKELY_COMMAND", None)
    if name is None:
        raise ChangeError("MERKELY_COMMAND environment-variable is not set.")
    print(f"MERKELY_COMMAND={name}")
    klass = build_command(name)
    command = klass(context)
    for env_var in command.env_vars:
        env_var.value
    return command()


def main(*, env=None, docker_fingerprinter=None, file_fingerprinter=None):
    try:
        run(env=env, docker_fingerprinter=docker_fingerprinter, file_fingerprinter=file_fingerprinter)
        print('Success')
        return 0
    except ChangeError as exc:
        print(f"Error: {str(exc)}")
        return 144


