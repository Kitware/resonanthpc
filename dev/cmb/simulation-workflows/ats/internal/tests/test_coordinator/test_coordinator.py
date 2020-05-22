import os
import unittest

from writer import ats_writer, coordinator_writer

from tests.base import BaseTestCase


class CoordinatorTest(BaseTestCase):

    ATT_RESOURCE_FILENAME = 'att.coordinator.smtk'
    BASLINE_XML_FILENAME = 'baseline_coordinator.xml'
    SOURCE_DIR = os.path.abspath(os.path.dirname(__file__))

    def test_coordinator(self):
        coordinator_writer.CoordinatorWriter().write(self.writer.xml_root)
        xml_string = self.writer.get_xml_doc(pretty=True)
        self._compare_xml_content(xml_string)


if __name__ == '__main__':
    unittest.main()
