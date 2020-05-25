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
        r"${VALUE}": FLOAT_FORMAT.format(att.find("value").value()),
    }
    return mapping


def map_independent_variable_function(att):
    # TODO: the domain section can also be "rest domian" or "domain rain"

    vals = att.find("x-values")
    x_value_list = [vals.value(i) for i in range(vals.numberOfValues())]
    x_value_list = [str(x) for x in x_value_list]
    x_values = r"{" + ','.join(x_value_list) + r"}"

    vals = att.find("y-values")
    y_value_list = [vals.value(i) for i in range(vals.numberOfValues())]
    y_value_list = [str(x) for x in y_value_list]
    y_values = r"{" + ','.join(y_value_list) + r"}"

    mapping = {
        r"${NAME}": att.name(),
        r"${CONSTANT_IN_TIME}": 'true' if  att.find("constant in time").isEnabled() else 'false',
        r"${REGION}": att.findComponent('region').value().name(),
        # TODO: forcing these for now.
        r"${COMPONENT_NAME}": "components",
        r"${COMPONENT_TYPE}": "Array(string)",
        r"${COMPONENTS}": "{" + str(att.find("components").value()) + "}",
        r"${X_VALUES}": x_values,
        r"${Y_VALUES}": y_values,
    }
    return mapping


def map_eos(att):
    mapping = {
        r"${NAME}": att.name(),
        r"${EOS_BASIS}": str(att.find("EOS basis").value()),
        r"${MOLAR_DENSITY_KEY}": str(att.find("molar density key").value()),
        r"${MASS_DENSITY_KEY}": str(att.find("mass density key").value()),
        r"${EOS_TYPE}": "liquid water",
    }
    return mapping


def map_eos_constant(att):
    mapping = map_eos(att)
    mapping.update({
        r"${EOS_TYPE}": "constant",
        r"${KEY}": str(att.find("key").value()),
        r"${VALUE}": FLOAT_FORMAT.format(att.find("value").value()),
    })
    return mapping


def map_eos_vapor(att):
    mapping = map_eos(att)
    mapping.update({
        r"${EOS_TYPE}": "vapor in gas",
    })
    return mapping


def map_compressible_porosity(att):
    mapping = {
        r"${NAME}": att.name(),
        r"${REGION}": att.findComponent('region').value().name(),
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
            "independent variable - function": ("fe-independent-variable-function.xml", map_independent_variable_function),
            "eos": ("fe-eos.xml", map_eos),
            "eos-constant": ("fe-eos-constant.xml", map_eos_constant),
            "eos-vapor": ("fe-eos-vapor.xml", map_eos_vapor),
            "compressible porosity": ("fe-compressible-porosity.xml", map_compressible_porosity),
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
