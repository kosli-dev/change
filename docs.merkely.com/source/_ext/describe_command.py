from docutils import nodes
from docutils.parsers.rst import Directive
from commands import COMMANDS, Context


class DescribeCommand(Directive):

    has_content = True

    def run(self):
        args = self.content[0].split()
        name = args[0]
        description_type = args[1]
        if description_type == "summary":
            return command_summary(name)
        if description_type == "invocation":
            return command_invocation(name)
        if description_type == "parameters":
            return command_parameters(name)
        return []


def command_summary(name):
    return [nodes.paragraph(text=command_for(name).summary)]


def command_invocation(name):
    return [nodes.literal_block(text=command_for(name).invocation)]


def command_parameters(name):
    return [env_vars_to_table(command_for(name).env_vars)]


def command_for(name):
    env = {"MERKELY_COMMAND": name}
    context = Context(env, None, None)
    return COMMANDS[name](context)


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


def setup(app):
    app.add_directive("describe_command", DescribeCommand)
    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }