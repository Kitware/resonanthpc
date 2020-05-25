import os
import sys
import unittest

from writer import ats_writer, checkpoint_writer

from tests.base import BaseTestCase

class CheckpointTest(BaseTestCase):

    BASELINE_XML_FILENAME = 'baseline_checkpoint.xml'
    SOURCE_DIR = os.path.abspath(os.path.dirname(__file__))
    YAML_RESOURCE = 'checkpoint.yml'

    def test_checkpoint(self):
        checkpoint_writer.CheckpointWriter().write(self.writer.xml_root)
        xml_string = self.writer.get_xml_doc(pretty=True)
        self._compare_xml_content(xml_string)


if __name__ == '__main__':
    unittest.main()
