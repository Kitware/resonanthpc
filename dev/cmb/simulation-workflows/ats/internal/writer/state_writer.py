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
from .base_writer import BaseWriter, FLOAT_FORMAT
from .templates.creator import append_template


def map_independent_variable(att):
    # TODO: the domain section can also be "rest domian" or "domain rain"
    mapping = {
        r"${NAME}": att.name(),
        r"${CONSTANT_IN_TIME}": 'true' if  att.find("constant in time").isEnabled() else 'false',
        r"${REGION}": att.findComponent('region').value().name(),
        # TODO: forcing these for now.
        r"${COMPONENT_NAME}": "components",
        r"${COMPONENT_TYPE}": "Array(string)",
        r"${COMPONENTS}": "{" + str(att.find("components").value()) + "}",
        r"${VALUE}": FLOAT_FORMAT.format(att.find("value").value())
    }
    return mapping


def map_eos(att):
    # <Parameter name="density [kg/m^3]" type="double" value="1000.0" />

    # <ParameterList name="gas EOS parameters" type="ParameterList">
    #   <Parameter name="EOS type" type="string" value="ideal gas" />
    # </ParameterList>

    # TODO: hard coding for demo 01

    mapping = {
        r"${NAME}": att.name(),
        r"${EOS_BASIS}": "both",
        r"${MOLAR_DENSITY_KEY}": "molar_density_liquid",
        r"${MASS_DENSITY_KEY}": "mass_density_liquid",
        r"${EOS_TYPE}": "liquid water",
        r"${ADDITIONAL_EOS_PARAMETERS}": "",
    }
    return mapping


class StateWriter(BaseWriter):
    """Writer for ATS state output lists."""
    def __init__(self):
        super(StateWriter, self).__init__()


    def write(self, xml_root):
        """Perform the XML write out."""
        state_elem = self._new_list(xml_root, 'state')

        #### handle field evaluators
        fe_elem = self._new_list(state_elem, 'field evaluators')

        basic_templates = {
            "capillary pressure, atmospheric gas over liquid": "fe-capillary-pressure.xml",
            "effective_pressure": "fe-effective-pressure.xml",
            "richards water content": "fe-richards-water-content.xml",
            "viscosity": "fe-viscosity.xml",
            "molar fraction gas": "fe-molar-fraction-gas.xml",
            "overland pressure water content": "fe-overland-pressure-water-content.xml",
            "ponded depth": "fe-ponded-depth.xml",
            "ponded depth bar": "fe-ponded-depth-bar.xml",
        }


        smart_templates = {
            "independent variable": ("fe-independent-variable.xml", map_independent_variable),
            "eos": ("fe-eos.xml", map_eos),
        }

        fe_atts = shared.sim_atts.findAttributes('field-evaluator-base')
        for att in fe_atts:
            name = att.name()
            fe_type = att.type()
            if fe_type in basic_templates:
                append_template(fe_elem, basic_templates[fe_type], {r"${NAME}": name})
            elif fe_type in smart_templates:
                # We gotta be smart
                fname, func = smart_templates[fe_type]
                mapping = func(att)
                append_template(fe_elem, fname, mapping)
            else:
                pass # not implemented



        #### handle the initial conditions
        ic_elem = self._new_list(state_elem, 'initial conditions')

        known_children = [
            "value",
        ]

        ic_atts = shared.sim_atts.findAttributes('ic-base')
        for att in ic_atts:
            name = att.name()
            ic_list_elem = self._new_list(ic_elem, name)
            self._render_items(ic_list_elem, att, known_children)

        return
