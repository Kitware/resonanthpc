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


TAB_SPACING = '  '


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

    def write(self, output_filepath=None):
        """Generate the xml output file.

        Return:
            True if output file written
            False if output file failed to write
            None if no output file specified
        """
        self.generate_xml()

        # Write output file
        if output_filepath is not None:
            wrote_file = False
            with open(output_filepath, 'w') as fp:
                xml_string = shared.xml_doc.toprettyxml(indent=TAB_SPACING)
                fp.write(xml_string)
                wrote_file = True
            return wrote_file

        # (else)
        return None


    def setup_xml_root(self):
        shared.initialize(self.sim_atts, minidom.Document())

        self.xml_root = shared.xml_doc.createElement('ParameterList')
        self.xml_root.setAttribute('name', 'Main')
        self.xml_root.setAttribute('type', 'ParameterList')
        shared.xml_doc.appendChild(self.xml_root)
        return


    def get_xml_doc(self, pretty=False):
        if pretty:
            content = shared.xml_doc.toprettyxml(indent=TAB_SPACING)
            formatted = ""
            for line in content.splitlines():
                line = line.rstrip()
                if len(line) > 0:
                    formatted += (line + "\n")
            return formatted
        return shared.xml_doc


    def generate_xml(self):
        """Builds xml document from current sim_atts resource.

        Returns shared.xml_doc for testing
        """
        self.setup_xml_root()

        from . import domain_writer
        imp.reload(domain_writer)
        domain_writer.DomainWriter().write(self.xml_root)

        from . import region_writer
        imp.reload(region_writer)
        region_writer.RegionWriter().write(self.xml_root)

        ################################

        ## TODO: implement other writers

        ################################
        return shared.xml_doc
