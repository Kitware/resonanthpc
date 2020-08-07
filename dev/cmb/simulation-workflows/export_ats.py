# =============================================================================
#
#  Copyright (c) Kitware, Inc.
#  All rights reserved.
#  See LICENSE.txt for details.
#
#  This software is distributed WITHOUT ANY WARRANTY; without even
#  the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
#  PURPOSE.  See the above copyright notice for more information.
#
# =============================================================================

"""Command line program to write ATS input file"""


import argparse
import os
import sys

top_dir = os.path.join(
    os.path.dirname(__file__), os.pardir, os.pardir, os.pardir,
)
path = os.path.join(top_dir, "smtk-tools",)
utilities_module_path = os.path.normpath(path)
sys.path.insert(0, utilities_module_path)
from smtk_tools.resource_io import ResourceIO

import smtk
import smtk.attribute
import smtk.io
import smtk.operation
import smtk.resource
import smtk.session.vtk

OPERATION_SUCCEEDED = int(smtk.operation.Operation.SUCCEEDED)  # 3


def read_resource(op_manager, path):
    """"""
    read_op = op_manager.createOperation('smtk::operation::ReadResource')
    read_op.parameters().find('filename').setValue(path)
    read_result = read_op.operate()
    read_outcome = read_result.findInt('outcome').value(0)
    if read_outcome != OPERATION_SUCCEEDED:
        raise RuntimeError('Failed to load {}, outcome {}'.format(path, read_outcome))
    resource = read_result.find('resource').value()
    if resource is None:
        raise RuntimeError('Resource is None ({})'.format(path))
    return resource


def import_python_op(op_manager, path):
    """"""
    import_op = op_manager.createOperation('smtk::operation::ImportPythonOperation')
    import_op.parameters().find('filename').setValue(path)
    import_result = import_op.operate()
    import_outcome = import_result.findInt('outcome').value(0)
    if import_outcome != OPERATION_SUCCEEDED:
        raise RuntimeError('Failed to load export operator: {}, outcome {}'.format(path, import_outcome))

    op_unique_name = import_result.findString("unique_name").value()
    op = op_manager.createOperation(op_unique_name)
    return op


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate ATS input file from attribute resource')
    parser.add_argument('attribute_filepath', help='Input attribute filename/path (.smtk)')
    parser.add_argument('--model_filepath', '-m', help='path to SMTK model resource (.smtk)')
    parser.add_argument('--output_filepath', '-o', default='ats_input.xml', help='output filename/path (ats_input.xml)')
    parser.add_argument('--export_operation', '-e', default='ats/ats.py', help='export operation path (./ats/ats.py)')

    args = parser.parse_args()
    # print(args)

    # Initialize smtk managers
    res_manager = smtk.resource.Manager.create()
    op_manager = smtk.operation.Manager.create()
    smtk.attribute.Registrar.registerTo(res_manager)
    smtk.attribute.Registrar.registerTo(op_manager)
    smtk.operation.Registrar.registerTo(op_manager)
    op_manager.registerResourceManager(res_manager)

    my_dir = os.path.abspath(os.path.dirname(__file__))

    # Initialize ResourceIO and load resources
    model_resource = None
    if args.model_filepath:
        mfile = os.path.abspath(args.model_filepath)
        assert os.path.exists(mfile)
        model_resource = read_resource(op_manager, mfile)
        assert model_resource is not None, 'failed to load model resource from file {}'.format(mfile)

    # Load the export operator
    path_list = args.export_operation.split(os.sep)
    op_path = os.path.join(my_dir, *path_list)
    print('op_path:', op_path)
    export_op = import_python_op(op_manager, op_path)

    # Load the attribute resource
    att_resource = read_resource(op_manager, args.attribute_filepath)
    if model_resource:
        att_resource.associate(model_resource)

    # Configure the export operator
    params = export_op.parameters()
    res_item = params.findResource('attributes')
    res_item.setValue(att_resource)
    file_item = params.findFile('output-file')
    if os.path.isabs(args.output_filepath):
        output_path = args.output_filepath
    else:
        output_path = os.path.join(os.getcwd(), args.output_filepath)
    file_item.setValue(output_path)

    export_result = export_op.operate()
    sys.stdout.flush()
    export_outcome = export_result.findInt('outcome').value(0)
    if export_outcome != OPERATION_SUCCEEDED:
        raise RuntimeError('export operator failed, outcome {}'.format(export_outcome))

    print('finish')
    sys.exit(0)
