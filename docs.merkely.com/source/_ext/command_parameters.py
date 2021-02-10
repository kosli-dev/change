from docutils import nodes
from docutils.parsers.rst import Directive

from commands import COMMANDS, Context


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
        name = self.content[0]
        return [command_env_table(name)]


def setup(app):
    app.add_directive("command_parameters", CommandParameters)

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }