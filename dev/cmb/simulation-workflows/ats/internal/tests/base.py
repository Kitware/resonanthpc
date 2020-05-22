import os
import unittest

import smtk
import smtk.attribute
import smtk.io
import smtk.operation
import smtk.resource
import smtk.session.vtk

from writer import ats_writer


OPERATION_SUCCEEDED = int(smtk.operation.Operation.SUCCEEDED)  # 3


class BaseTestCase(unittest.TestCase):
    """A Base test case class to handle SMTK manager stuff."""

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

        # Load resource files
        atts_path = os.path.join(self.SOURCE_DIR, self.ATT_RESOURCE_FILENAME)
        self.att_resource = self._read_resource(atts_path)

        # Initialize writer
        self.writer = ats_writer.ATSWriter(self.att_resource)
        self.writer.setup_xml_root()

    def tearDown(self):
        self.res_manager = None
        self.op_manager = None
        self.att_resource = None
        self.model_resource = None

    def _read_resource(self, path):
        read_op = self.op_manager.createOperation('smtk::operation::ReadResource')
        read_op.parameters().find('filename').setValue(path)
        read_result = read_op.operate()
        read_outcome = read_result.findInt('outcome').value(0)
        self.assertEqual(read_outcome, OPERATION_SUCCEEDED)
        resource = read_result.find('resource').value()
        self.assertIsNotNone(resource)
        return resource

    def _read_baseline(self, baseline_path):
        """A helper in case we want to change how we read the XML."""
        with open(baseline_path) as fp:
            baseline_string = fp.read()
        return baseline_string

    def _compare_xml_content(self, xml_string):
        """A helper in case we want to get fancier in how we compare the XML."""
        baseline_path = os.path.join(self.SOURCE_DIR, self.BASLINE_XML_FILENAME)
        baseline_string = self._read_baseline(baseline_path)
        self.assertEqual(xml_string, baseline_string)
        return
