import os
import unittest

from tests.base import BaseTestCase


class SpinupHomoTest(BaseTestCase):

    MODEL_RESOURCE_FILENAME = "data/mesh.rock_creek.smtk"
    BASELINE_XML_FILENAME = "spinup-homo.xml"
    SOURCE_DIR = os.path.abspath(os.path.dirname(__file__))
    YAML_RESOURCE = "spinup-homo.yml"

    def test(self):
        self.writer.generate_xml()
        xml_string = self.writer.get_xml_doc(pretty=True)
        self._compare_xml_content(xml_string)


class TemplateTest(BaseTestCase):

    MODEL_RESOURCE_FILENAME = "data/mesh.rock_creek.smtk"
    BASELINE_XML_FILENAME = "template.xml"
    SOURCE_DIR = os.path.abspath(os.path.dirname(__file__))
    YAML_RESOURCE = "template.yml"

    def test(self):
        self.writer.generate_xml()
        xml_string = self.writer.get_xml_doc(pretty=True)
        self._compare_xml_content(xml_string)


if __name__ == "__main__":
    unittest.main()
