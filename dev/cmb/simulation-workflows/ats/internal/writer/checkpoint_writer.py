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


class CheckpointWriter(BaseWriter):
    """Writer for ATS checkpoint output lists."""

    def __init__(self):
        super(CheckpointWriter, self).__init__()

    def write(self, xml_root):
        """Perform the XML write out."""
        # possible children parameters
        known_children = [
            "file name base",
            "file name digits",
        ]

        check_elem = self._new_list(xml_root, "checkpoint")
        check_inst = shared.sim_atts.findAttribute("checkpoint driver")

        # Now populate that list with all the attributes - no sub lists
        self._render_items(check_elem, check_inst, known_children)

        # Now handle the IO Event spec group all in this main list
        io_event = check_inst.find("checkpoint times")
        self._render_io_event_specs(check_elem, io_event)
        return
