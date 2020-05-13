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


class VisualizationWriter(BaseWriter):
    """Writer for ATS visualization output lists."""
    def __init__(self):
        super(VisualizationWriter, self).__init__()


    def write(self, xml_root):
        """Perform the XML write out."""
        # possible children parameters
        known_children = [
            'file name base',
            'dynamic mesh',
        ]

        vis_elem = self._new_list(xml_root, 'visualization')
        vis_atts = shared.sim_atts.findAttributes('visualization driver')
        for att in vis_atts:
            # Outermost element is ParameterList with name of domain/mesh
            name = att.find('domain').name()
            domain_list_elem = self._new_list(vis_elem, name)

            # Now populate that list with all the attributes - no sub lists
            self._render_items(domain_list_elem, att, known_children)

            # Now handle the IO Event spec group all in this main list
            io_event = att.find('visualization times')
            self._render_io_event_specs(domain_list_elem, io_event)
        return
