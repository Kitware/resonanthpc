import os
import unittest

from writer import ats_writer, vis_writer

from tests.base import BaseTestCase


class VisualizationEventTest(BaseTestCase):

    ATT_RESOURCE_FILENAME = 'att.vis.smtk'
    BASLINE_XML_FILENAME = 'baseline_vis.xml'
    SOURCE_DIR = os.path.abspath(os.path.dirname(__file__))

    def test_vis_event(self):
        vis_writer.VisualizationWriter().write(self.writer.xml_root)
        xml_string = self.writer.get_xml_doc(pretty=True)
        self._compare_xml_content(xml_string)


if __name__ == '__main__':
    unittest.main()
