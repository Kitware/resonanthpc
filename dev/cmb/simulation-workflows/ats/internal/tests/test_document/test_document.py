import os
import unittest

import smtk
import smtk.attribute

from writer import ats_writer


class DocumentTest(unittest.TestCase):
    def test_document(self):
        """"""
        # Load baseline
        source_dir = os.path.abspath(os.path.dirname(__file__))
        baseline_path = os.path.join(source_dir, "baseline_document.xml")
        baseline_string = None
        with open(baseline_path) as fp:
            baseline_string = fp.read()
        self.assertIsNotNone(baseline_string)

        # Generate document from empty attribute resource
        sim_atts = smtk.attribute.Resource.create()
        writer = ats_writer.ATSWriter(sim_atts)
        xml_doc = writer.generate_xml()
        xml_string = xml_doc.toprettyxml(indent="  ")
        self.assertEqual(xml_string, baseline_string)


if __name__ == "__main__":
    unittest.main()
