import os
import unittest

from writer import ats_writer, state_writer

from tests.base import BaseTestCase

ATT_RESOURCE_FILENAME = 'att.state.smtk'
BASLINE_XML_FILENAME = 'baseline_state.xml'

class StateTest(BaseTestCase):

    def test_state(self):
        """"""
        source_dir = os.path.abspath(os.path.dirname(__file__))

        # Load resource files
        atts_path = os.path.join(source_dir, ATT_RESOURCE_FILENAME)
        self.att_resource = self._read_resource(atts_path)

        # Generate xml
        writer = ats_writer.ATSWriter(self.att_resource)
        writer.setup_xml_root()
        state_writer.StateWriter().write(writer.xml_root)
        xml_string = writer.get_xml_doc(pretty=True)

        baseline_path = os.path.join(source_dir, BASLINE_XML_FILENAME)
        baseline_string = self._read_baseline(baseline_path)
        self._compare_xml_content(xml_string, baseline_string)


if __name__ == '__main__':
    unittest.main()
