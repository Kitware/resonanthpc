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
from .templates.creator import append_template


def map_richards_steady_state(att):
    bc_assocs = att.associations()
    value_list = list()
    for i in range(bc_assocs.numberOfValues()):
        if bc_assocs.isSet(i):
            value_att = bc_assocs.value(i)
            value_list.append(value_att.name())

    mapping = {
        r"${NAME}": att.name(),
        r"${BC_REGIONS}": r"{" + ", ".join(value_list) + r"}",
        r"${IC_REGION}": att.findComponent('initial condition').value().name(),
        r"${WRE_REGION}": att.findComponent('water retention evaluator').value().name(),
    }
    return mapping



class PKWriter(BaseWriter):
    """Writer for ATS process kernel trees."""
    def __init__(self):
        super(PKWriter, self).__init__()


    def write(self, xml_root):
        """Perform the XML write out."""
        pks_elem = self._new_list(xml_root, 'PKs')

        smart_templates = {
            "pk-richards" : ("pk-richards-steady-state.xml", map_richards_steady_state)
        }

        pk_atts = shared.sim_atts.findAttributes('pk-base')
        for att in pk_atts:
            name = att.name()
            pk_type = att.type()
            if pk_type in smart_templates:
                # We gotta be smart
                fname, func = smart_templates[pk_type]
                mapping = func(att)
                append_template(pks_elem, fname, mapping)
            else:
                pass # not implemented


        return
