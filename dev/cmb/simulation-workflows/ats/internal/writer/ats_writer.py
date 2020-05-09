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

import imp
import os
print('loading', os.path.basename(__file__))
from xml.dom import minidom

import smtk
import smtk.attribute

from .shared_data import instance as shared

from . import base_writer
imp.reload(base_writer)
from .base_writer import BaseWriter


class ATSWriter(BaseWriter):
    """Top level writer for ATS input files."""

    def __init__(self, sim_atts):
        """Initializes the exporter class with the simulation parameters.

        Inputs:
          sim_atts: attribute resource specifying simulation
        """
        super(ATSWriter, self).__init__()
        self.sim_atts = sim_atts
        self.xml_root = None

    def write(self, output_filepath):
        """Generate the xml output file."""
        shared.initialize(self.sim_atts, minidom.Document())

        self.xml_root = shared.xml_doc.createElement('ParameterList')
        self.xml_root.setAttribute('name', 'Main')
        self.xml_root.setAttribute('type', 'ParameterList')
        shared.xml_doc.appendChild(self.xml_root)


        ################################

        # self._generate_domains_xml()
        from . import domain_writer
        imp.reload(domain_writer)
        domain_writer.DomainWriter().write(self.xml_root)


        self._generate_regions_xml()
        ## TODO: uncomment as implemented
        # self._generate_cycle_driver_xml()
        # self._generate_visualization_xml()
        # self._generate_observations_xml()
        # self._generate_checkpoint_xml()
        # self._generate_pks_xml()
        # self._generate_state_xml()

        ################################

        # Write output file
        wrote_file = False
        with open(output_filepath, 'w') as fp:
            xml_string = shared.xml_doc.toprettyxml(indent=" ")
            fp.write(xml_string)
            wrote_file = True
        return wrote_file

    #### This section contains methods to write each Main element ####

    def _generate_regions_xml(self):
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

        regions_elem = self._new_list(self.xml_root, 'regions')
        region_atts = shared.sim_atts.findAttributes('region')
        for region_att in region_atts:
            # Outermost element is ParameterList with name of region
            name_list_elem = self._new_list(regions_elem, region_att.name(), None)

            # Next level is ParameterList with type of region
            region_type = region_att.type()
            param_name = region_type_params.get(region_type)
            if param_name is None:
                param_name = region_type.replace('.', ': ')
            type_list_elem = self._new_list(name_list_elem, param_name, None)

            # surface.labeled is special case
            if region_type.startswith('region.labeled'):
                ats_entity_types = {
                    'region.labeled.volume': 'cell',
                    'region.labeled.surface': 'face',
                    'region.labeled.edge': 'edge',
                    'region.labeled.vertex': 'node',
                }

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

                entity_string = ats_entity_types.get(region_type, 'unknown')
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


        return

    def _generate_cycle_driver_xml(self):
        raise NotImplementedError()

    def _generate_visualization_xml(self):
        raise NotImplementedError()

    def _generate_observations_xml(self):
        raise NotImplementedError()

    def _generate_checkpoint_xml(self):
        raise NotImplementedError()

    def _generate_pks_xml(self):
        raise NotImplementedError()

    def _generate_state_xml(self):
        raise NotImplementedError()
