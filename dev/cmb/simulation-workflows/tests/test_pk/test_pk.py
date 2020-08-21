import os
import unittest

from writer import pk_writer

from tests.base import BaseTestCase


class PKTest(BaseTestCase):

    BASELINE_XML_FILENAME = "baseline_pk.xml"
    SOURCE_DIR = os.path.abspath(os.path.dirname(__file__))
    YAML_RESOURCE = "pk.yml"

    def test_pk(self):
        pk_writer.PKWriter().write(self.writer.xml_root)
        xml_string = self.writer.get_xml_doc(pretty=True)
        self._compare_xml_content(xml_string)


if __name__ == "__main__":
    unittest.main()
