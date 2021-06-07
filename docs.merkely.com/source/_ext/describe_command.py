from docutils import nodes
from docutils.parsers.rst import Directive
from commands import Command, External
from docs import compound_para


class DescribeCommand(Directive):

    has_content = True

    def run(self):
        args = self.content[0].split()
        command_name = args[0]
        description_type = args[1]
        ci_name = args[2]
        if description_type == "summary":
            return summary(command_name)
        if description_type == "invocation_full":
            return invocation_full(command_name, ci_name)
        if description_type == "invocation_minimum":
            return invocation_minimum(command_name)
        if description_type == "parameters":
            return parameters(command_name, ci_name)
        return []


def summary(command_name):
    text = command_for(command_name).doc_summary()
    return [compound_para(nodes, text)]


# The Makefile volume-mounts docs.merkely.com/ to docs/
REFERENCE_DIR = '/docs/build/reference'


def invocation_full(command_name, ci_name):
    filename = f"{REFERENCE_DIR}/{ci_name}/{command_name}.txt"
    with open(filename, "rt") as file:
        text = file.read()

    command = command_for(command_name)

    div = nodes.container()
    add_literal_block_link(div, command, ci_name)

    # div += nodes.literal_block('', '', nodes.raw(text, text, format='bash'))
    div += nodes.literal_block(rawsource=text, text=text, format='yaml')
    div += parameters(command, ci_name)


    div_classes = [ci_name, "tab-pane"]
    if ci_name == "docker":
        div_classes.append("active")
    div.update_basic_atts({
        "ids": [ci_name],
        "classes": div_classes
    })
    return [div]


def invocation_minimum(command_name):
    filename = f"{REFERENCE_DIR}/min/{command_name}.txt"
    with open(filename, "rt") as file:
        text = file.read()
    return [nodes.literal_block(text=text)]


def parameters(command, ci_name):
    env_vars = command.merkely_env_vars
    return [env_vars_to_table(env_vars, ci_name, command.name.value)]


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
    row += nodes.entry("", nodes.paragraph(text="ENV_VAR_NAME"))
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
            para = nodes.paragraph(text="The artifact's ")
            para += nodes.reference('', 'Fingerprint', internal=False, refuri=ref)
            row += nodes.entry("", para)
        else:
            para = compound_para(nodes, note)
            row += nodes.entry("", para)
        tbody += row
    tgroup += tbody
    return table


def add_literal_block_link(div, command, ci_name):
    ref = command.doc_ref()
    result = ref.get(ci_name, None)
    if result is not None:
        f = result[0]
        s = result[1]
        ref = f(s)
        para = nodes.paragraph(text="")
        text = 'Open an example, similar to the fragment below, from a git repo.'
        para += nodes.reference('', text, internal=False, refuri=ref)
        para.update_basic_atts({
            # See docs.merkely.com/source/_static/merkely-custom.js for how
            # a target="_block" is added to this <a href="...>
            # See docs.merkely.com/source/_static/merkely-custom.css for styling.
            "classes": ['literal-block-link']
        })
        div += para


def setup(app):
    app.add_directive("describe_command", DescribeCommand)
    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }