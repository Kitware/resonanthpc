import os
import unittest

from writer import ats_writer, state_writer

from tests.base import BaseTestCase


class StateTest(BaseTestCase):

    BASELINE_XML_FILENAME = 'baseline_state.xml'
    SOURCE_DIR = os.path.abspath(os.path.dirname(__file__))
    YAML_RESOURCE = 'state.yml'

    def test_state(self):
        state_writer.StateWriter().write(self.writer.xml_root)
        xml_string = self.writer.get_xml_doc(pretty=True)
        self._compare_xml_content(xml_string)


if __name__ == '__main__':
    unittest.main()
