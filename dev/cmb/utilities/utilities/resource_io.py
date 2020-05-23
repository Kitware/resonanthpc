import os
import sys

import smtk
import smtk.attribute
import smtk.io
import smtk.operation
import smtk.resource
import smtk.session.vtk


OPERATION_SUCCEEDED = int(smtk.operation.Operation.SUCCEEDED)  # 3

class ResourceIO:
    """A class for SMTK resource file import, read and write functions."""

    def __init__(self):
        """"""
        self.att_resource = None
        self.op_manager = None
        self.res_manager = None
        self.spec = None

        # Initialize smtk managers
        self.res_manager = smtk.resource.Manager.create()
        self.op_manager = smtk.operation.Manager.create()
        smtk.attribute.Registrar.registerTo(self.res_manager)
        smtk.attribute.Registrar.registerTo(self.op_manager)
        smtk.session.vtk.Registrar.registerTo(self.res_manager)
        smtk.session.vtk.Registrar.registerTo(self.op_manager)
        smtk.operation.Registrar.registerTo(self.op_manager)
        self.op_manager.registerResourceManager(self.res_manager)

    def import_resource(self, path):
        """Imports native file into new SMTK resource.

        Works with attribute templates and models that can be
        loaded by smtk.session.vtk
        """
        import_op = self.op_manager.createOperation('smtk::operation::ImportResource')
        import_op.parameters().find('filename').setValue(path)
        result = import_op.operate()
        outcome = result.findInt('outcome').value()
        assert outcome == OPERATION_SUCCEEDED
        resource = result.find('resource').value()
        assert resource is not None
        return resource

    def read_resource(self, path):
        """Reads SMTK resource file (*.smtk).

        Works with attribute resources and model resources of type smtk.session.vtk
        """
        read_op = self.op_manager.createOperation('smtk::operation::ReadResource')
        read_op.parameters().find('filename').setValue(path)
        result = read_op.operate()
        outcome = result.findInt('outcome').value()
        assert outcome == OPERATION_SUCCEEDED
        resource = result.find('resource').value()
        assert resource is not None
        return resource

    def write_resource(self, resource, path=None):
        """"""
        write_op = self.op_manager.createOperation('smtk::operation::WriteResource')
        write_op.parameters().associate(resource)
        if path is not None:
            write_op.parameters().find('filename').setIsEnabled(True)
            write_op.parameters().find('filename').setValue(path)

        write_result = write_op.operate()
        outcome = write_result.findInt('outcome').value()
        assert outcome == OPERATION_SUCCEEDED
