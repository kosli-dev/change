import os
import sys
sys.path.append(os.path.abspath("/app/source"))
import doc_gen
from pyfakefs.fake_filesystem_unittest import TestCase


class AutoGenerateReferenceRstFilesTestCase(TestCase):
    def setUp(self):
        self.setUpPyfakefs()

    def test_auto_generate(self):
        os.makedirs(doc_gen.REFERENCE_DIR)
        doc_gen.auto_generate_rst_files()
        # TODO: assert rst files exist
