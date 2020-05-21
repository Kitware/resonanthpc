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


class StateWriter(BaseWriter):
    """Writer for ATS state output lists."""
    def __init__(self):
        super(StateWriter, self).__init__()


    def write(self, xml_root):
        """Perform the XML write out."""
        state_elem = self._new_list(xml_root, 'state')

        #### handle field evaluators
        # TODO
        fe_elem = self._new_list(xml_root, 'field evaluators')


        #### handle the initial conditions
        ic_elem = self._new_list(xml_root, 'initial conditions')

        known_children = [
            "value",
        ]

        ic_atts = shared.sim_atts.findAttributes('ic-base')
        for att in ic_atts:
            name = att.find('name').value()
            print(name)
            ic_list_elem = self._new_list(ic_elem, name)
            self._render_items(ic_list_elem, att, known_children)

        return
