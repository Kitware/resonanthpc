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

print("loading", os.path.basename(__file__))
from xml.dom import minidom

import smtk
import smtk.attribute

from .shared_data import instance as shared
from .base_writer import BaseWriter


class ObservationWriter(BaseWriter):
    """Writer for ATS observation output lists."""

    def __init__(self):
        super(ObservationWriter, self).__init__()

    def write(self, xml_root):
        """Perform the XML write out."""
        # possible children parameters
        known_children = [
            "observation output filename",
            "variable",
            "delimiter",
            "location name",
            "functional",
            "direction normalized flux",
            "write interval",
        ]

        obs_elem = self._new_list(xml_root, "observations")
        obs_atts = shared.sim_atts.findAttributes("observation")
        for att in obs_atts:
            # Outermost element is ParameterList with name of the attribute
            name = att.name()
            obs_list_elem = self._new_list(obs_elem, name)

            # Now populate that list with all the attributes - no sub lists
            self._render_items(obs_list_elem, att, known_children)

            # Add the region name
            region_name = att.find("region").value().name()
            self._new_param(obs_list_elem, "region", "string", region_name)

            # Now handle the IO Event spec group all in this main list
            io_event = att.find("observation times")
            self._render_io_event_specs(obs_list_elem, io_event)
        return
