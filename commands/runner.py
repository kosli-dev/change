from commands import Context, build_command, CommandError


def run(env=None, docker_fingerprinter=None, file_fingerprinter=None):
    context = Context(env, docker_fingerprinter, file_fingerprinter)
    command = build_command(context)
    print(f"MERKELY_COMMAND={command.name.value}")
    command.check()
    return command()


def main(env=None, docker_fingerprinter=None, file_fingerprinter=None):
    try:
        run(env, docker_fingerprinter, file_fingerprinter)
        return 0
    except CommandError as exc:
        print(f"Error: {str(exc)}")
        return 144


