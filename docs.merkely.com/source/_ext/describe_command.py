from docutils import nodes
from docutils.parsers.rst import Directive
from commands import COMMANDS, External


class DescribeCommand(Directive):

    has_content = True

    def run(self):
        args = self.content[0].split()
        name = args[0]
        description_type = args[1]
        if len(args) <= 2:
            ci = 'docker'  # 'github', 'bitbucket'
        else:
            ci = args[2]
        if description_type == "summary":
            return summary(name)
        if description_type == "invocation_full":
            return invocation(name, 'full')
        if description_type == "invocation_minimum":
            return invocation(name, 'minimum')
        if description_type == "parameters":
            return parameters(name, ci)
        return []


def summary(name):
    return [nodes.paragraph(text=command_for(name).summary)]


def invocation(name, kind):
    return [nodes.literal_block(text=command_for(name).invocation(kind))]


def parameters(name, ci):
    return [env_vars_to_table(command_for(name).merkely_env_vars, ci)]


def command_for(name):
    env = {"MERKELY_COMMAND": name}
    context = External(env=env)
    return COMMANDS[name](context)


def env_vars_to_table(env_vars, ci):
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
    row += nodes.entry("", nodes.paragraph(text="Required?"))
    row += nodes.entry("", nodes.paragraph(text="Notes"))
    thead += row

    tbody = nodes.tbody()
    for env_var in env_vars:
        row = nodes.row()
        row += nodes.entry("", nodes.paragraph(text=env_var.name))
        if env_var.is_required(ci):
            required = 'yes'
        else:
            required = 'no'
        row += nodes.entry("", nodes.paragraph(text=required))
        notes = env_var.notes(ci)
        if notes == "<FINGERPRINT_LINK>":
            ref = "../../fingerprints/docker_fingerprint.html"
            para = nodes.paragraph(text="")
            para += nodes.reference('', 'Fingerprint', internal=False, refuri=ref)
            row += nodes.entry("", para)
        else:
            row += nodes.entry("", nodes.paragraph(text=notes))
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