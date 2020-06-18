import os
import unittest

from writer import ats_writer, vis_writer

from tests.base import BaseTestCase



class RockCreekSpinupHomoTest(BaseTestCase):
    """

    pysmtk build_attributes.py ../dev/cmb/simulation-workflows/ats/ats.sbt ../dev/cmb/simulation-workflows/ats/internal/tests/test_rock_creek/rock_creek.spinup.homo.yml -m ../dev/cmb/simulation-workflows/ats/internal/tests/test_rock_creek/att.rock_creek.mesh.smtk -o ../rock_creek.smtk

    """

    MODEL_RESOURCE_FILENAME = 'att.rock_creek.mesh.smtk'
    BASELINE_XML_FILENAME = 'baseline_rock_creek_spinup.homo.xml'
    SOURCE_DIR = os.path.abspath(os.path.dirname(__file__))
    YAML_RESOURCE = 'rock_creek.spinup_homo.yml'

    def test(self):
        xml_doc = self.writer.generate_xml()
        xml_string = self.writer.get_xml_doc(pretty=True)
        self._compare_xml_content(xml_string)


if __name__ == '__main__':
    unittest.main()
