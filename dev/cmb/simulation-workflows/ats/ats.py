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
"""
Export operator for ATS workflows
"""

import imp
import os
import sys
import traceback

import smtk
import smtk.attribute
import smtk.io
import smtk.operation

# Add the directory containing this file to the python module search list
import inspect
source_file = os.path.abspath(inspect.getfile(inspect.currentframe()))
sys.path.insert(0, os.path.dirname(source_file))
# Make sure __file__ is set when using modelbuilder
__file__ = source_file
print('loading', os.path.basename(__file__))

import internal
import internal.writer
imp.reload(internal.writer)  # for development


class Export(smtk.operation.Operation):
    """"""
    def __init__(self):
        smtk.operation.Operation.__init__(self)

    def name(self):
        return "Export ATS"

    def operateInternal(self):
        try:
            success = ExportCMB(self)
        except Exception as e:
            print("\n\nERROR:")
            track = traceback.format_exc()
            print(track)
            print("\n\n")
            #smtk.ErrorMessage(self.log(), sys.exc_info()[0])
            raise
            return self.createResult(smtk.operation.Operation.Outcome.FAILED)

        # Return with success
        result = self.createResult(smtk.operation.Operation.Outcome.SUCCEEDED)
        result.find('success').setValue(int(success))
        return result

    def createSpecification(self):
        spec = self.createBaseSpecification()
        # print('spec:', spec)

        # Load export atts
        source_dir = os.path.abspath(os.path.dirname(__file__))
        # print('source_dir:', source_dir)
        sbt_path = os.path.join(source_dir, 'internal', 'ats-export.sbt')
        print('sbt_path:', sbt_path)
        reader = smtk.io.AttributeReader()
        result = reader.read(spec, sbt_path, self.log())
        # print('reader result:', result)

        # Setup result definition
        resultDef = spec.createDefinition('test result', 'result')
        successDef = smtk.attribute.IntItemDefinition.New('success')
        resultDef.addItemDefinition(successDef)

        return spec


def ExportCMB(export_op):
    """Entry function, called by export operator"""
    params = export_op.parameters()
    logger = export_op.log()

    # Get the simulation attribute resource
    sim_atts = smtk.attribute.Resource.CastTo(params.find('attributes').value())
    if sim_atts is None:
        msg = 'ERROR - No simulation attributes'
        print(msg)
        raise RuntimeError(msg)

    # Get output filepath
    output_file_item = params.findFile('output-file')
    output_file = output_file_item.value(0)

    # Create output folder if needed
    output_dir = os.path.dirname(output_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    from internal.writer import ats_writer
    imp.reload(ats_writer)

    writer = ats_writer.ATSWriter(sim_atts)
    completed = writer.write(output_file)
    print('Writer completion status: %s' % completed)

    # In some runtime environments, stdout is null
    if sys.stdout is not None:
        sys.stdout.flush()

    # print('ats.py number of warnings:', len(writer.warning_messages))
    # for msg in writer.warning_messages:
    #     logger.addWarning(msg)

    return completed
