import os
import sys
import unittest

import smtk
import smtk.attribute
import smtk.io
import smtk.operation
import smtk.resource
import smtk.session.vtk

from writer import ats_writer, vis_writer

ATT_RESOURCE_FILENAME = 'att.vis.smtk'
# BASLINE_XML_FILENAME = 'baseline_vis.xml'

OPERATION_SUCCEEDED = int(smtk.operation.Operation.SUCCEEDED)  # 3

class VisualizationEventTest(unittest.TestCase):

    def setUp(self):
        self.att_resource = None
        self.model_resource = None

        # Initialize smtk managers
        self.res_manager = smtk.resource.Manager.create()
        self.op_manager = smtk.operation.Manager.create()

        smtk.attribute.Registrar.registerTo(self.res_manager)
        smtk.attribute.Registrar.registerTo(self.op_manager)

        smtk.session.vtk.Registrar.registerTo(self.res_manager)
        smtk.session.vtk.Registrar.registerTo(self.op_manager)

        smtk.operation.Registrar.registerTo(self.op_manager)
        self.op_manager.registerResourceManager(self.res_manager)

    def tearDown(self):
        self.res_manager = None
        self.op_manager = None
        self.att_resource = None
        self.model_resource = None

    def test_vis_event(self):
        """"""
        source_dir = os.path.abspath(os.path.dirname(__file__))

        # Load resource files
        atts_path = os.path.join(source_dir, ATT_RESOURCE_FILENAME)
        self.att_resource = self._read_resource(atts_path)


        # Generate xml
        writer = ats_writer.ATSWriter(self.att_resource)
        writer.setup_xml_root()
        vis_writer.VisualizationWriter().write(writer.xml_root)
        xml_string = writer.get_xml_doc(pretty=True)

        # TODO: Compare xml
        with open(os.path.join(source_dir, 'foo.xml'), 'w') as fout:
            fout.write(xml_string)
        # baseline_path = os.path.join(source_dir, BASLINE_XML_FILENAME)
        # with open(baseline_path) as fp:
        #     baseline_string = fp.read()
        # self.assertEqual(xml_string, baseline_string)

    def _read_resource(self, path):
        read_op = self.op_manager.createOperation('smtk::operation::ReadResource')
        read_op.parameters().find('filename').setValue(path)
        read_result = read_op.operate()
        read_outcome = read_result.findInt('outcome').value(0)
        self.assertEqual(read_outcome, OPERATION_SUCCEEDED)
        resource = read_result.find('resource').value()
        self.assertIsNotNone(resource)
        return resource


if __name__ == '__main__':
    unittest.main()
