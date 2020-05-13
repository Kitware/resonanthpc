import os
import unittest

from writer import ats_writer

from tests.base import BaseTestCase

ATT_RESOURCE_FILENAME = 'att.mesh_regions.smtk'
MODEL_RESOURCE_FILENAME = 'model.concave.smtk'
BASLINE_XML_FILENAME = 'baseline_mesh_regions.xml'


class MeshRegionsTest(BaseTestCase):

    def test_mesh_regions(self):
        """"""
        source_dir = os.path.abspath(os.path.dirname(__file__))

        # Load resource files
        atts_path = os.path.join(source_dir, ATT_RESOURCE_FILENAME)
        self.att_resource = self._read_resource(atts_path)

        model_path = os.path.join(source_dir, os.pardir, 'data', MODEL_RESOURCE_FILENAME)
        self.model_resource = self._read_resource(model_path)

        # Generate xml
        writer = ats_writer.ATSWriter(self.att_resource)
        xml_doc = writer.generate_xml()
        xml_string = xml_doc.toprettyxml(indent='  ')

        # Compare xml
        baseline_path = os.path.join(source_dir, BASLINE_XML_FILENAME)
        with open(baseline_path) as fp:
            baseline_string = fp.read()
        self.assertEqual(xml_string, baseline_string)


if __name__ == '__main__':
    unittest.main()
