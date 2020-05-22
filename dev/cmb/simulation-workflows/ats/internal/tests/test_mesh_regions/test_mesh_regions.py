import os
import unittest

from writer import ats_writer, domain_writer, region_writer

from tests.base import BaseTestCase


class MeshRegionsTest(BaseTestCase):

    ATT_RESOURCE_FILENAME = 'att.mesh_regions.smtk'
    MODEL_RESOURCE_FILENAME = 'model.concave.smtk'
    BASLINE_XML_FILENAME = 'baseline_mesh_regions.xml'
    SOURCE_DIR = os.path.abspath(os.path.dirname(__file__))

    def test_mesh_regions(self):
        model_path = os.path.join(self.SOURCE_DIR, os.pardir, 'data', self.MODEL_RESOURCE_FILENAME)
        self.model_resource = self._read_resource(model_path)

        domain_writer.DomainWriter().write(self.writer.xml_root)
        region_writer.RegionWriter().write(self.writer.xml_root)
        xml_string = self.writer.get_xml_doc(pretty=True)
        self._compare_xml_content(xml_string)


if __name__ == '__main__':
    unittest.main()
