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

import smtk
import smtk.attribute
import smtk.io
import smtk.operation
import smtk.resource

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

    # Load the export operator
    path_list = args.export_operation.split(os.sep)
    op_path = os.path.join(my_dir, *path_list)
    print('op_path:', op_path)
    export_op = import_python_op(op_manager, op_path)

    # Load the attribute resource
    att_resource = read_resource(op_manager, args.attribute_filepath)

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
