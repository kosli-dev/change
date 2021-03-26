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
            return invocation_full(name, ci)
        if description_type == "invocation_minimum":
            return invocation_minimum(name)
        if description_type == "parameters":
            return parameters(name, ci)
        return []


def summary(name, ci):
    return [nodes.paragraph(text=command_for(name).summary(ci))]


# The Makefile volume-mounts docs.merkely.com/ to docs/
REFERENCE_DIR = '/docs/build/reference'


def invocation_full(name, ci):
    filename = f"{REFERENCE_DIR}/{ci}/{name}.txt"
    with open(filename, "rt") as file:
        text = file.read()

    div = nodes.container()
    div += nodes.literal_block(text=text)
    div += parameters(name, ci)

    # Add bootstrap "tab-pane" to connect to
    #    <ul class="nav nav-tabs">...</ul>
    # inside each command's .rst file

    div_classes = [ci, "tab-pane"]
    if ci == "docker":
        div_classes.append("active")
    div.update_basic_atts({
        "ids": [ci],
        "classes": div_classes
    })
    return [div]


def invocation_minimum(name):
    filename = f"{REFERENCE_DIR}/min/{name}.txt"
    with open(filename, "rt") as file:
        text = file.read()
    return [nodes.literal_block(text=text)]


def parameters(command_name, ci):
    return [env_vars_to_table(command_for(command_name).merkely_env_vars, ci, command_name)]


def command_for(name):
    cls = Command.named(name)
    env = {"MERKELY_COMMAND": name}
    external = External(env=env)
    return cls(external)


def env_vars_to_table(env_vars, ci_name, command_name):
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
    row += nodes.entry("", nodes.paragraph(text="ENV-VARS"))
    row += nodes.entry("", nodes.paragraph(text="Required?"))
    row += nodes.entry("", nodes.paragraph(text="Notes"))
    thead += row

    tbody = nodes.tbody()
    for env_var in env_vars:
        row = nodes.row()
        row += nodes.entry("", nodes.paragraph(text=env_var.name))
        if env_var.is_required(ci_name):
            required = 'yes'
        else:
            required = 'no'
        row += nodes.entry("", nodes.paragraph(text=required))
        note = env_var.doc_note(ci_name, command_name)
        if note == "<FINGERPRINT_LINK>":
            ref = "../../fingerprints/docker_fingerprint.html"
            para = nodes.paragraph(text="")
            para += nodes.reference('', 'Fingerprint', internal=False, refuri=ref)
            row += nodes.entry("", para)
        else:
            row += nodes.entry("", nodes.paragraph(text=note))
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