import os
import sys
import unittest

from writer import ats_writer, checkpoint_writer

from tests.base import BaseTestCase

ATT_RESOURCE_FILENAME = 'att.checkpoint.smtk'
# BASLINE_XML_FILENAME = 'baseline_vis.xml'

class CheckpointTest(BaseTestCase):

    def test_checkpoint(self):
        """"""
        source_dir = os.path.abspath(os.path.dirname(__file__))

        # Load resource files
        atts_path = os.path.join(source_dir, ATT_RESOURCE_FILENAME)
        self.att_resource = self._read_resource(atts_path)


        # Generate xml
        writer = ats_writer.ATSWriter(self.att_resource)
        writer.setup_xml_root()
        checkpoint_writer.CheckpointWriter().write(writer.xml_root)
        xml_string = writer.get_xml_doc(pretty=True)

        # TODO: Compare xml
        with open(os.path.join(source_dir, 'foo.xml'), 'w') as fout:
            fout.write(xml_string)
        # baseline_path = os.path.join(source_dir, BASLINE_XML_FILENAME)
        # with open(baseline_path) as fp:
        #     baseline_string = fp.read()
        # self.assertEqual(xml_string, baseline_string)


if __name__ == '__main__':
    unittest.main()
