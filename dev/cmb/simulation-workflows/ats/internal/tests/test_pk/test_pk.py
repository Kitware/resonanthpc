import os
import unittest

from writer import ats_writer, pk_writer

from tests.base import BaseTestCase


class PKTest(BaseTestCase):

    ATT_RESOURCE_FILENAME = 'att.pk.smtk'
    BASLINE_XML_FILENAME = 'baseline_pk.xml'
    SOURCE_DIR = os.path.abspath(os.path.dirname(__file__))

    def test_pk(self):
        pk_writer.PKWriter().write(self.writer.xml_root)
        xml_string = self.writer.get_xml_doc(pretty=True)
        self._compare_xml_content(xml_string)


if __name__ == '__main__':
    unittest.main()
