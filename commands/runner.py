from commands import build_command, Context, CommandError


def run(env=None, docker_fingerprinter=None, file_fingerprinter=None):
    context = Context(env, docker_fingerprinter, file_fingerprinter)
    name = context.env.get("MERKELY_COMMAND", None)
    if name is None:
        raise CommandError("MERKELY_COMMAND environment-variable is not set.")
    print(f"MERKELY_COMMAND={name}")
    klass = build_command(name)
    command = klass(context)
    command.check()
    return command()


def main(env=None, docker_fingerprinter=None, file_fingerprinter=None):
    try:
        run(env, docker_fingerprinter, file_fingerprinter)
        print('Success')
        return 0
    except CommandError as exc:
        print(f"Error: {str(exc)}")
        return 144


