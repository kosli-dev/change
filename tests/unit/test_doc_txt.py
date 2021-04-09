import os
import sys
sys.path.append(os.path.abspath("/app/source"))
from docs import create_data, doc_txt
from pyfakefs.fake_filesystem_unittest import TestCase


class AutoGenerateReferenceTextFilesTestCase(TestCase):
    def setUp(self):
        self.setUpPyfakefs()

    def test_auto_generate(self):
        data = create_data()
        doc_txt.create_txt_files(data)
        # TODO: assert txt files exist

    def test_generate_docs(self):
        data = create_data()
        docs = doc_txt.generate_docs(data)
        assert "/docs/build/reference/github/log_test.txt" in docs.keys()

