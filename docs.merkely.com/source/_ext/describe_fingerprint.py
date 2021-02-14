from docutils import nodes
from docutils.parsers.rst import Directive
from fingerprinters import build_fingerprinter


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
    return [nodes.paragraph(text=build_fingerprinter(name).notes)]


def example(name):
    return [nodes.literal_block(text=build_fingerprinter(name).example)]


def setup(app):
    app.add_directive("describe_fingerprint", DescribeFingerprint)
    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }