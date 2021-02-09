from commands import COMMANDS, Context


def living_docs():
    env = {}
    context = Context(env, None, None)
    command = COMMANDS['log_evidence'](context)
    for env_var in command.env_vars:
        print(f"{env_var.name} {env_var.type} {env_var.description}")


if __name__ == '__main__':
    print(living_docs())
