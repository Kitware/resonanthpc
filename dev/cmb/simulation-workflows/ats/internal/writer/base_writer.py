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

"""Common base class for writers"""

import os
print('loading', os.path.basename(__file__))
from xml.dom import minidom

import smtk
import smtk.attribute
import smtk.model

from .shared_data import instance as shared

TypeStringMap = {
    smtk.attribute.Item.DoubleType: 'double',
    smtk.attribute.Item.IntType: 'int',
    smtk.attribute.Item.StringType: 'string',
    smtk.attribute.Item.VoidType: 'bool',
    smtk.attribute.Item.FileType: 'string',
}


class BaseWriter:
    """Base writer class for ATS input files.

    Should ONLY contain methods (no member data)
    """

    def __init__(self):
        """"""
        # Do NOT include any member data
        pass

    def _get_native_model_path(self, resource):
        """"""
        # We only support model resource filenames for now
        model_res = smtk.model.Resource.CastTo(resource)
        if model_res is None:
            return None

        # Unfortunately, this logic is all part of SMTK lore.
        uuids = model_res.entitiesMatchingFlags(smtk.model.MODEL_ENTITY, True)
        if not uuids:
            raise RuntimeError('No model entities in model resource')

        model_uuid = uuids.pop()
        if not model_res.hasStringProperty(model_uuid, 'url'):
            raise RuntimeError('Model resource missing \"url\" property')
        prop_list = model_res.stringProperty(model_uuid, 'url')
        return prop_list[0]

    def _new_list(self, parent, list_name, list_type='ParameterList'):
        """Appends ParameterList element to parent"""
        new_list = shared.xml_doc.createElement('ParameterList')
        new_list.setAttribute('name', list_name)
        new_list.setAttribute('type', list_type)
        parent.appendChild(new_list)
        return new_list

    def _new_param(self, list_elem, param_name, param_type, param_value):
        """Appends Parameter element to list_elem"""
        new_param = shared.xml_doc.createElement('Parameter')
        new_param.setAttribute('name', param_name)
        new_param.setAttribute('type', param_type)
        new_param.setAttribute('value', param_value)
        list_elem.appendChild(new_param)
        return new_param

    def _render_associations(self, parent_elem, att, elem_name_or_list):
        """Generates Parameter element for attribute associations."""
        ref_item = att.associations()
        if ref_item is None:
            print('Warning: expected attribute \"{}\" to have associations'.format(att.name()))
            return

        n = ref_item.numberOfValues()
        if n == 0:
            print('Warning: expected attribute \"{}\" to have associations'.format(att.name()))
            return

        if isinstance(elem_name_or_list, (list, tuple)) and len(elem_name_or_list) > 1:
            elem_name = elem_name_or_list[0]
            array_name = elem_name_or_list[1]
        else:
            elem_name = elem_name_or_list
            array_name = elem_name

        # Generate list of attribute names
        value_list = list()
        for i in range(n):
            if ref_item.isSet(i):
                value_att = ref_item.value(i)
                value_list.append(value_att.name())

        if len(value_list) == 0:
            print('Warning: expected attribute \"{}\" to have associations'.format(att.name()))
            return

        if len(value_list) == 1:
            self._new_param(parent_elem, elem_name, 'string', value_list[0])
            return

        # (else) n > 1
        value_string = ', '.join(value_list)
        array_string = '{{{}}}'.format(value_string)
        self._new_param(parent_elem, array_name, 'Array(string)', array_string)

    def _render_items(self, parent_elem, att, param_names):
        """Generates Parameter elements for items specified by param_names"""
        assert isinstance(param_names, list)
        for param_name in param_names:
            item = att.find(param_name)
            if item is None:
                continue

            # TODO: we need to handle `ComponentType`

            # skip over optional items if not enabled. Bools are never optional... weird logic here.
            if item.type() != smtk.attribute.Item.VoidType and not item.isEnabled():
                continue

            type_string = TypeStringMap.get(item.type())
            value = None
            if item.type() == smtk.attribute.Item.VoidType:
                value = 'true' if item.isEnabled() else 'false'
            elif hasattr(item, 'numberOfValues') and item.numberOfValues() > 1:
                type_string = 'Array({})'.format(type_string)
                value_list = list()
                for i in range(item.numberOfValues()):
                    value_list.append(item.value(i))
                string_list = [str(x) for x in value_list]
                value = r"{" + ', '.join(string_list) + r"}"
            elif hasattr(item, 'value'):
                value = item.value()

            ####
            if value is None or not isinstance(value, str):
                raise NotImplementedError("({}) for ({}) is not handled".format(item.type(), param_name))

            self._new_param(parent_elem, param_name, type_string, value)
        return


