from docutils import nodes
from docutils.parsers.rst import Directive
from commands import Command, External


class DescribeCommand(Directive):

    has_content = True

    def run(self):
        args = self.content[0].split()
        name = args[0]
        description_type = args[1]
        ci = args[2]
        if description_type == "summary":
            return summary(name, ci)
        if description_type == "invocation_full":
            return invocation(name, 'full', ci)
        if description_type == "invocation_minimum":
            return invocation(name, 'minimum', ci)
        if description_type == "parameters":
            return parameters(name, ci)
        return []


def summary(name, ci):
    return [nodes.paragraph(text=command_for(name).summary(ci))]


def invocation(name, kind, ci):
    return [nodes.literal_block(text=command_for(name).invocation(kind, ci))]


def parameters(name, ci):
    return [env_vars_to_table(command_for(name).merkely_env_vars, ci)]


def command_for(name):
    cls = Command.named(name)
    env = {"MERKELY_COMMAND": name}
    external = External(env=env)
    return cls(external)


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