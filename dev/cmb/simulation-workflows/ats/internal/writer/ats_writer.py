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

TypeStringMap = {
    smtk.attribute.Item.DoubleType: 'double',
    smtk.attribute.Item.IntType: 'int',
    smtk.attribute.Item.StringType: 'string',
    smtk.attribute.Item.VoidType: 'bool',
    smtk.attribute.Item.FileType: 'string',
}


class ATSWriter:
    """Top level writer class for ATS input files."""

    def __init__(self, export_params):
        """Initializes the exporter class with the simulation parameters.
        """
        self.checked_attributes = set()  # attributes that have been validated
        self.model_resource = None
        self.sim_atts = None
        self.warning_messages = list()
        self.xml_doc = None
        self.xml_root = None

        self.sim_atts = smtk.attribute.Resource.CastTo(export_params.find('attributes').value())
        # print('sim_atts', self.sim_atts)
        if self.sim_atts is None:
            msg = 'ERROR - No simulation attributes'
            print(msg)
            raise RuntimeError(msg)

    def write(self, output_filepath):
        """Generate the xml output file."""
        self.xml_doc = minidom.Document()
        self.xml_root = self.xml_doc.createElement('ParameterList')
        self.xml_root.setAttribute('name', 'Main')
        self.xml_root.setAttribute('type', 'ParameterList')
        self.xml_doc.appendChild(self.xml_root)


        ################################

        self._generate_domains_xml()
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
            xml_string = self.xml_doc.toprettyxml(indent=" ")
            fp.write(xml_string)
            wrote_file = True
        return wrote_file

    def _new_list(self, parent, list_name, list_type='ParameterList'):
        """Appends ParameterList element to parent"""
        new_list = self.xml_doc.createElement('ParameterList')
        new_list.setAttribute('name', list_name)
        new_list.setAttribute('type', list_type)
        parent.appendChild(new_list)
        return new_list

    def _new_param(self, list_elem, param_name, param_type, param_value):
        """Appends Parameter element to list_elem"""
        new_param = self.xml_doc.createElement('Parameter')
        new_param.setAttribute('name', param_name)
        new_param.setAttribute('type', param_type)
        new_param.setAttribute('value', param_value)
        list_elem.appendChild(new_param)
        return new_param

    def _render_items(self, parent_elem, att, param_names):
        """Generates Parameter elements for items specified by param_names"""
        for param_name in param_names:
            item = att.find(param_name)
            if item is None:
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

            self._new_param(parent_elem, param_name, type_string, value)
        return

    #### This section contains methods to write each Main element ####

    def _generate_domains_xml(self):
        # possible children parameters
        children = {
            'generate mesh': ['domain low coordinate', 'domain high coordinate', 'number of cells'],
            'read mesh file': ['file', 'format'],
            # TODO: `export mesh to file` is optional - don't include unless valid
            'surface': ['urface sideset name', 'export mesh to file', ], # TODO: more
            'subgrid': ['subgrid region name', 'entity kind', 'parent domain', 'flyweight mesh'],
            # TODO: column mesh
        }
        # TODO: some of the demo files do not have these - when should we include them and when not?
        #       other sim files have them under an `expert` param list??
        main_param_names = ['verify mesh', 'deformable mesh', 'partitioner']
        ####
        # Logic to render the mesh section
        mesh_elem = self._new_list(self.xml_root, 'mesh')
        domain_atts = self.sim_atts.findAttributes('domain')
        for domain_att in domain_atts:
            # save out each domain
            domain_elem = self._new_list(mesh_elem, domain_att.name())
            type_item = domain_att.findString('mesh type')
            mesh_type = type_item.value()
            _ = self._new_param(domain_elem, 'mesh type', 'string', mesh_type)
            #  Winging it here to generate the parameters list
            gen_params_list_name = '{} parameters'.format(mesh_type)
            gen_params_list = self._new_list(domain_elem, gen_params_list_name)
            known_children = children.get(mesh_type, [])
            self._render_items(gen_params_list, type_item, known_children)
            # Top level mesh parameters
            self._render_items(domain_elem, domain_att, main_param_names)
        return

    def _generate_regions_xml(self):
        # possible children parameters
        children = {
            'region: plane': ['point', 'normal',],
            'region: box': ['low coordinate', 'high coordinate',],
            'region: labeled set': ['label', 'file', 'entity',],
            'region: color function': ['file', 'value',],
            'region: point': ['point',],
            'region: logical': ['operation',],
            # TODO: there's more to fill in here!
        }
        ####
        # Logic to render it - shouldn't need any changes
        regions_elem = self._new_list(self.xml_root, 'regions')
        region_atts = self.sim_atts.findAttributes('region')
        for region_att in region_atts:
            list_elem = self._new_list(regions_elem, region_att.name())
            type_list = self._new_list(list_elem, region_att.type())
            # Get list of known children for given attribute
            known_children = children.get(region_att.type(), [])
            self._render_items(type_list, region_att, known_children)
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
