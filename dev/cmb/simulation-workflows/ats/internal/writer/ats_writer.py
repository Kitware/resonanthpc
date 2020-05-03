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

from . import shared
imp.reload(shared)

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
        self.xml_root = None

        # Initialize shared data
        shared.checked_attributes = set()  # attributes that have been validated
        shared.model_resource = None
        shared.sim_atts = sim_atts
        shared.warning_messages = list()
        shared.xml_doc = None

    def write(self, output_filepath):
        """Generate the xml output file."""
        shared.xml_doc = minidom.Document()
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
        region_atts = shared.sim_atts.findAttributes('region')
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
