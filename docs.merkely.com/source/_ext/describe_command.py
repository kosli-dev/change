from docutils import nodes
from docutils.parsers.rst import Directive

from commands import COMMANDS, Context


def command_summary(name):
    env = {"MERKELY_COMMAND": name}
    context = Context(env, None, None)
    command = COMMANDS[name](context)
    return [nodes.paragraph(text=command.summary)]


def command_invocation(name):
    env = {"MERKELY_COMMAND": name}
    context = Context(env, None, None)
    command = COMMANDS[name](context)
    return [nodes.literal_block(text=command.invocation)]


def command_env_table(name):
    env = {"MERKELY_COMMAND": name}
    context = Context(env, None, None)
    command = COMMANDS[name](context)
    return env_vars_to_table(command.env_vars)


def env_vars_to_table(env_vars):
    table = nodes.table()
    tgroup = nodes.tgroup(cols=3)
    table += tgroup

    colspec = nodes.colspec()
    tgroup += colspec
    tgroup += colspec
    tgroup += colspec

    thead = nodes.thead()
    tgroup += thead
    row = nodes.row()
    row += nodes.entry("", nodes.paragraph(text="NAME"))
    row += nodes.entry("", nodes.paragraph(text="Type"))
    row += nodes.entry("", nodes.paragraph(text="Description"))
    thead += row

    tbody = nodes.tbody()
    for env_var in env_vars:
        row = nodes.row()
        row += nodes.entry("", nodes.paragraph(text=env_var.name))
        row += nodes.entry("", nodes.paragraph(text=env_var.type))
        if env_var.description == "<FINGERPRINT_LINK>":
            pass
        else:
            row += nodes.entry("", nodes.paragraph(text=env_var.description))
        tbody += row
    tgroup += tbody
    return table


class CommandParameters(Directive):

    has_content = True

    def run(self):
        name = self.content[0].split()[0]
        description_type = self.content[0].split()[1]
        if description_type == "parameters":
            return [command_env_table(name)]
        if description_type == "invocation":
            return command_invocation(name)
        if description_type == "summary":
            return command_summary(name)
        return []


def setup(app):
    app.add_directive("describe_command", CommandParameters)

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }