import os
import unittest

from writer import ats_writer, vis_writer

from tests.base import BaseTestCase

ATT_RESOURCE_FILENAME = 'att.vis.smtk'
BASLINE_XML_FILENAME = 'baseline_vis.xml'

class VisualizationEventTest(BaseTestCase):

    def test_vis_event(self):
        """"""
        source_dir = os.path.abspath(os.path.dirname(__file__))

        # Load resource files
        atts_path = os.path.join(source_dir, ATT_RESOURCE_FILENAME)
        self.att_resource = self._read_resource(atts_path)

        # Generate xml
        writer = ats_writer.ATSWriter(self.att_resource)
        writer.setup_xml_root()
        vis_writer.VisualizationWriter().write(writer.xml_root)
        xml_string = writer.get_xml_doc(pretty=True)

        baseline_path = os.path.join(source_dir, BASLINE_XML_FILENAME)
        baseline_string = self._read_baseline(baseline_path)
        self._compare_xml_content(xml_string, baseline_string)


if __name__ == '__main__':
    unittest.main()
