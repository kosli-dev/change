from docutils import nodes
from docutils.parsers.rst import Directive

from commands import COMMANDS, Context


def log_evidence_env_table():
    name = 'log_evidence'
    env = {"MERKELY_COMMAND": name}
    context = Context(env, None, None)
    command = COMMANDS[name](context)
    return env_vars_to_table(command.env_vars)


def env_vars_to_table(env_vars):
    table = nodes.table()
    tgroup = nodes.tgroup(cols=3)
    table += tgroup

    colspec = nodes.colspec(colwidth=100)
    tgroup += colspec
    tgroup += colspec
    tgroup += colspec

    tbody = nodes.tbody()
    for env_var in env_vars:
        row = nodes.row()
        row += nodes.entry("", nodes.paragraph(text=env_var.name))
        row += nodes.entry("", nodes.paragraph(text=env_var.type))
        row += nodes.entry("", nodes.paragraph(text=env_var.description))
        tbody += row
    tgroup += tbody
    return table


class HelloWorld(Directive):

    def run(self):
        log_evidence = log_evidence_env_table()
        return [log_evidence]


def setup(app):
    app.add_directive("helloworld", HelloWorld)

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }