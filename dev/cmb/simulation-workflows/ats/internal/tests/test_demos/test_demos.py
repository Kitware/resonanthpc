import os
import unittest

from writer import ats_writer, vis_writer

from tests.base import BaseTestCase


class Demo01Test(BaseTestCase):

    BASELINE_XML_FILENAME = "baseline_demo_01.xml"
    SOURCE_DIR = os.path.abspath(os.path.dirname(__file__))
    YAML_RESOURCE = "demo.01.yml"

    def test_demo(self):
        xml_doc = self.writer.generate_xml()
        xml_string = self.writer.get_xml_doc(pretty=True)
        self._compare_xml_content(xml_string)


class Demo02Test(BaseTestCase):

    BASELINE_XML_FILENAME = "baseline_demo_02.xml"
    SOURCE_DIR = os.path.abspath(os.path.dirname(__file__))
    YAML_RESOURCE = "demo.02.yml"

    def test_demo(self):
        xml_doc = self.writer.generate_xml()
        xml_string = self.writer.get_xml_doc(pretty=True)
        self._compare_xml_content(xml_string)

#
# class Demo03Test(BaseTestCase):
#
#     BASELINE_XML_FILENAME = "baseline_demo_03.xml"
#     SOURCE_DIR = os.path.abspath(os.path.dirname(__file__))
#     YAML_RESOURCE = "demo.03.yml"
#
#     def test_demo(self):
#         xml_doc = self.writer.generate_xml()
#         xml_string = self.writer.get_xml_doc(pretty=True)
#         self._compare_xml_content(xml_string)
#
#
# class Demo04Test(BaseTestCase):
#
#     MODEL_RESOURCE_FILENAME = "att.demo.04.mesh.smtk"
#     BASELINE_XML_FILENAME = "baseline_demo_04.xml"
#     SOURCE_DIR = os.path.abspath(os.path.dirname(__file__))
#     YAML_RESOURCE = "demo.04.yml"
#
#     def test_demo(self):
#         xml_doc = self.writer.generate_xml()
#         xml_string = self.writer.get_xml_doc(pretty=True)
#         self._compare_xml_content(xml_string)


if __name__ == "__main__":
    unittest.main()
