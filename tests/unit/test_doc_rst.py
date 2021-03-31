import os
import sys
sys.path.append(os.path.abspath("/app/source"))
from docs import doc_rst
from pyfakefs.fake_filesystem_unittest import TestCase


class AutoGenerateReferenceRstFilesTestCase(TestCase):
    def setUp(self):
        self.setUpPyfakefs()

    def test_auto_generate(self):
        os.makedirs(doc_rst.REFERENCE_DIR)
        doc_rst.create_rst_files()
        # TODO: assert rst files exist
