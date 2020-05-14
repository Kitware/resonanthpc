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


class CoordinatorWriter(BaseWriter):
    """Writer for ATS coordinator (cycle driver)."""
    def __init__(self):
        super(CoordinatorWriter, self).__init__()


    def write(self, xml_root):
        """Perform the XML write out."""
        # possible children parameters
        known_children = [
            'start time',
            'start time units',
            'restart from checkpoint file',
            'wallclock duration [hrs]',
        ]

        end_spec_opts = {
            'time': ['end time', 'end time units',],
            'cylce': ['end cycle',],
        }

        coord_elem = self._new_list(xml_root, 'cylce driver')
        coord_inst = shared.sim_atts.findAttribute('cycle driver')

        # Now populate that list with all the attributes - no sub lists
        self._render_items(coord_elem, coord_inst, known_children)

        # Now handle the end-spec
        end_spec = coord_inst.find('end-spec')
        childs = end_spec_opts[end_spec.value()]
        self._render_items(coord_elem, end_spec, childs)

        # Now handle the IO Event spec group all in this main list
        io_event = coord_inst.find('required times') # NOTE: this is optional
        if io_event.isEnabled():
            io_elem = self._new_list(xml_root, 'required times')
            self._render_io_event_specs(io_elem, io_event)

        # And now handle the PK tree which can get pretty complicated
        raise NotImplementedError('PK tree linking is non-trivial and seems we did not do it exactly right in the templates.')
        return
