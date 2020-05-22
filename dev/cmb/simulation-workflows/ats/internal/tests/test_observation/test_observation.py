import os
import unittest

from writer import ats_writer, observation_writer

from tests.base import BaseTestCase


class ObservationEventTest(BaseTestCase):

    ATT_RESOURCE_FILENAME = 'att.observation.smtk'
    BASLINE_XML_FILENAME = 'baseline_observation.xml'
    SOURCE_DIR = os.path.abspath(os.path.dirname(__file__))

    def test_observation_event(self):
        observation_writer.ObservationWriter().write(self.writer.xml_root)
        xml_string = self.writer.get_xml_doc(pretty=True)
        self._compare_xml_content(xml_string)


if __name__ == '__main__':
    unittest.main()
