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

import os
print('loading', os.path.basename(__file__))
import xml.etree.ElementTree as ET

import smtk
import smtk.attribute


class ATSWriter:
    """Top level writer class for ATS input files."""

    def __init__(self, export_params):
        """"""
        self.checked_attributes = set()  # attributes that have been validated
        self.elem_root = None
        self.elem_tree = None
        self.model_resource = None
        self.sim_atts = None
        self.warning_messages = list()

        self.sim_atts = smtk.attribute.Resource.CastTo(export_params.find('attributes').value())
        # print('sim_atts', self.sim_atts)
        if self.sim_atts is None:
            msg = 'ERROR - No simulation attributes'
            print(msg)
            raise RuntimeError(msg)

    def write(self, output_filepath):
        """"""
        self.elem_root = ET.Element('ParameterList', attrib=dict(name='Main', type='ParameterList'))
        self.elem_tree = ET.ElementTree(element=self.elem_root)

        wrote_file = False
        with open(output_filepath, 'wb') as fp:
            encoding = 'us-ascii'
            self.elem_tree.write(fp, encoding=encoding)
            fp.write(bytearray('\n', encoding=encoding))
            print('Wrote', output_filepath)
            wrote_file = True

        return wrote_file

    def _new_list(self, parent, list_name, list_type):
        """Appends ParameterList element to parent"""
        new_list = parent.append('ParameterList')
        new_list.set('name', list_name)
        new_list.set('type', list_type)
        return new_list

    def _new_param(self, list_elem, param_name, param_type, param_value):
        """Appends Parameter element to list_elem"""
        new_param = list_elem.append('Parameter')
        new_param.set('name', param_name)
        new_param.set('type', param_type)
        new_param.set('value', param_value)
