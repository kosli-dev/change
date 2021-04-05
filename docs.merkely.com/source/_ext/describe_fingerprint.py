from docutils import nodes
from docutils.parsers.rst import Directive
from fingerprinters import build_fingerprinter
import re


class DescribeFingerprint(Directive):

    has_content = True

    def run(self):
        args = self.content[0].split()
        name = args[0]
        description_type = args[1]
        if description_type == "notes":
            return notes(name)
        if description_type == "example":
            return example(name)


def notes(name):
    notes = build_fingerprinter(name).notes
    return [compound_para(notes)]


def example(name):
    return [nodes.literal_block(text=build_fingerprinter(name).example)]


def setup(app):
    app.add_directive("describe_fingerprint", DescribeFingerprint)
    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }


def compound_para(text):
    # https://docutils.sourceforge.io/docs/ref/doctree.html
    # Allow living documentation notes in source/ to contain embedded rst
    para = nodes.paragraph(text="")
    regex = re.compile(r':code:`(?P<content>.*?)`')
    for part in re.split(r'(:code:`.*?`)', text):
        match = regex.match(part)
        if match is None:
            div = nodes.inline(text=part)
        else:
            div = nodes.inline(text=match.group('content'))
            div.update_basic_atts({"classes": ['inline-code']})
        para += div

    return para
