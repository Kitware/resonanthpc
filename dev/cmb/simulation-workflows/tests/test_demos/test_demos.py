import os
import unittest

from tests.base import BaseTestCase


class Demo01Test(BaseTestCase):

    BASELINE_XML_FILENAME = "baseline_demo_01.xml"
    SOURCE_DIR = os.path.abspath(os.path.dirname(__file__))
    YAML_RESOURCE = "demo.01.yml"

    def test_demo(self):
        self.writer.generate_xml()
        xml_string = self.writer.get_xml_doc(pretty=True)
        self._compare_xml_content(xml_string)


class Demo02Test(BaseTestCase):

    BASELINE_XML_FILENAME = "baseline_demo_02.xml"
    SOURCE_DIR = os.path.abspath(os.path.dirname(__file__))
    YAML_RESOURCE = "demo.02.yml"

    def test_demo(self):
        self.writer.generate_xml()
        xml_string = self.writer.get_xml_doc(pretty=True)
        self._compare_xml_content(xml_string)


class Demo03Test(BaseTestCase):

    BASELINE_XML_FILENAME = "baseline_demo_03.xml"
    SOURCE_DIR = os.path.abspath(os.path.dirname(__file__))
    YAML_RESOURCE = "demo.03.yml"

    def test_demo(self):
        self.writer.generate_xml()
        xml_string = self.writer.get_xml_doc(pretty=True)
        self._compare_xml_content(xml_string)


class Demo04VTest(BaseTestCase):

    MODEL_RESOURCE_FILENAME = "mesh.04_v.smtk"
    BASELINE_XML_FILENAME = "baseline_demo_04_v.xml"
    SOURCE_DIR = os.path.abspath(os.path.dirname(__file__))
    YAML_RESOURCE = "demo.04_v.yml"

    def test_demo(self):
        self.writer.generate_xml()
        xml_string = self.writer.get_xml_doc(pretty=True)
        self._compare_xml_content(xml_string)


class Demo04SuperSlabTest(BaseTestCase):

    MODEL_RESOURCE_FILENAME = "mesh.04_super_slab.smtk"
    BASELINE_XML_FILENAME = "baseline_demo_04_super_slab.xml"
    SOURCE_DIR = os.path.abspath(os.path.dirname(__file__))
    YAML_RESOURCE = "demo.04_super_slab.yml"

    def test_demo(self):
        self.writer.generate_xml()
        xml_string = self.writer.get_xml_doc(pretty=True)
        self._compare_xml_content(xml_string)


class Demo05SpinupGI(BaseTestCase):

    MODEL_RESOURCE_FILENAME = "mesh.05_hillslope_noduff.smtk"
    BASELINE_XML_FILENAME = "baseline_demo_05_spinup_gi.xml"
    SOURCE_DIR = os.path.abspath(os.path.dirname(__file__))
    YAML_RESOURCE = "demo.05_spinup_gi.yml"

    def test_demo(self):
        self.writer.generate_xml()
        xml_string = self.writer.get_xml_doc(pretty=True)
        self._compare_xml_content(xml_string, True)


if __name__ == "__main__":
    unittest.main()
