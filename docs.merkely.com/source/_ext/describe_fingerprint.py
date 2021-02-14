from docutils import nodes
from docutils.parsers.rst import Directive
from fingerprinters import build_fingerprinter


class DescribeFingerprint(Directive):

    has_content = True

    def run(self):
        args = self.content[0].split()
        name = args[0]
        return [nodes.paragraph(text=build_fingerprinter(name).notes)]


def setup(app):
    app.add_directive("describe_fingerprint", DescribeFingerprint)
    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }