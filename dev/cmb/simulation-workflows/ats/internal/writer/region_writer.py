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
from xml.dom import minidom

import smtk
import smtk.attribute

from .shared_data import instance as shared
from .base_writer import BaseWriter


class RegionWriter(BaseWriter):
    """Writer for ATS region elements."""
    def __init__(self):
        super(RegionWriter, self).__init__()

    def write(self, xml_root):
        """"""
        # Define names that are not directly function of attribute type
        region_type_params = {
            'region.labeled.surface': 'region: labeled set',
        }

        # Association parameters
        assoc_params = {
            'region.logical': 'regions',
            'region.labeled.surface': 'label',
        }

        # possible children parameters
        children = {
            'region.plane': ['point', 'normal',],
            'region.box': ['low coordinate', 'high coordinate',],
            'region.labeled.surface': ['label', 'file', 'entity',],
            'region.color-function': ['file', 'value',],
            'region.point': ['point',],
            'region.logical': ['operation',],
            # TODO: there's more to fill in here!
        }

        labeled_region_types = {
            'region.labeled.volume': 'cell',
            'region.labeled.surface': 'face',
            'region.labeled.edge': 'edge',
            'region.labeled.vertex': 'node',
        }

        regions_elem = self._new_list(xml_root, 'regions')
        region_atts = shared.sim_atts.findAttributes('region')
        for region_att in region_atts:
            # Outermost element is ParameterList with name of region
            name_list_elem = self._new_list(regions_elem, region_att.name())

            # Next level is ParameterList with type of region
            region_type = region_att.type()
            param_name = region_type_params.get(region_type)
            if param_name is None:
                param_name = region_type.replace('.', ': ')
            type_list_elem = self._new_list(name_list_elem, param_name)

            # surface.labeled is special case
            if region_type.startswith('region.labeled'):
                assoc_item = region_att.associations()
                model_entity = assoc_item.value()
                if model_entity is None:
                    raise RuntimeError('No model entity found for region attribute ()'.format(region_att.name()))
                resource = model_entity.resource()
                if resource is None:
                    raise RuntimeError('Model not loaded for ResourceItem {}'.format(item.name()))

                # Write "file" and "format"
                path = self._get_native_model_path(resource)
                if path is None:
                    raise RuntimeError('Model file not found for ResourceItem {}'.format(item.name()))
                # For now, just write the base filename
                filename = os.path.basename(path)
                self._new_param(type_list_elem, 'file', 'string', filename)
                # Todo Extend to include MSTK mesh files
                self._new_param(type_list_elem, 'format', 'string', 'Exodus II')

                entity_string = labeled_region_types.get(region_type, 'unknown')
                self._new_param(type_list_elem, 'entity', 'string', entity_string)

                # Should "label" instead be the pedigree id?
                # model_resource = smtk.model.Resource.CastTo(resource)
                # uuid = model_entity.id()
                # prop_list = model_resource.integerProperty(uuid, 'pedigree id')
                # pedigree_id = prop_list[0]
                # self._new_param(type_list_elem, 'label', 'string', str(pedigree_id))

                # For now, use the model_entity name
                self._new_param(type_list_elem, 'label', 'string', model_entity.name())
                continue

            # Get list of known children for given attribute
            known_children = children.get(region_att.type(), [])
            self._render_items(type_list_elem, region_att, known_children)

            # Association params
            assoc_params_list = assoc_params.get(region_type)
            if assoc_params_list:
                self._render_associations(type_list_elem, region_att, assoc_params_list)
