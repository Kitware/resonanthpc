import os
import sys
import unittest

import smtk
import smtk.attribute
import smtk.io
import smtk.operation
import smtk.resource
import smtk.session.vtk

from writer import ats_writer

ATT_RESOURCE_FILENAME = 'att.mesh_regions.smtk'
MODEL_RESOURCE_FILENAME = 'model.concave.smtk'
BASLINE_XML_FILENAME = 'baseline_mesh_regions.xml'

OPERATION_SUCCEEDED = int(smtk.operation.Operation.SUCCEEDED)  # 3

class MeshRegionsTest(unittest.TestCase):

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
