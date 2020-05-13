import unittest

import smtk
import smtk.attribute
import smtk.io
import smtk.operation
import smtk.resource
import smtk.session.vtk


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
