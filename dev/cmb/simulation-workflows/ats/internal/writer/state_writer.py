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

import smtk
import smtk.attribute

from .shared_data import instance as shared
from .base_writer import BaseWriter, FLOAT_FORMAT
from .templates.creator import append_template


def map_independent_variable(att):
    # TODO: the domain section can also be "rest domian" or "domain rain"
    mapping = {
        r"${NAME}": att.name(),
        r"${CONSTANT_IN_TIME}": 'true' if att.find("constant in time").isEnabled() else 'false',
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
    group = att.find('tabular-data')

    def _fetch_subgroup_values(group, name):
        values = []
        for i in range(group.numberOfGroups()):
            v = group.find(i, name, smtk.attribute.SearchStyle.IMMEDIATE)
            values.append(v.value())
        return values

    x_value_list = _fetch_subgroup_values(group, "X")
    x_value_list = [str(x) for x in x_value_list]
    x_values = r"{" + ','.join(x_value_list) + r"}"

    y_value_list = _fetch_subgroup_values(group, "Y")
    y_value_list = [str(x) for x in y_value_list]
    y_values = r"{" + ','.join(y_value_list) + r"}"

    mapping = {
        r"${NAME}": att.name(),
        r"${CONSTANT_IN_TIME}": 'true' if att.find("constant in time").isEnabled() else 'false',
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


class StateWriter(BaseWriter):
    """Writer for ATS state output lists."""
    def __init__(self):
        super(StateWriter, self).__init__()

    def render_richards_water_content(self, fe_elem, att):
        options = ['porosity key', 'molar density liquid key', 'saturation liquid key', 'cell volume key']
        self._render_items(fe_elem, att, options)

    def render_viscosity(self, fe_elem, att):
        options = ['viscosity key', 'temperature key',]
        self._render_items(fe_elem, att, options)
        # Sub group
        model_params = ['viscosity relation type',]
        model_params_elem = self._new_list(fe_elem, 'viscosity model parameters')
        self._render_items(model_params_elem, att, model_params)

    def render_capillary_pressure(self, fe_elem, att):
        pass

    def render_effective_pressure(self, fe_elem, att):
        pass

    def render_molar_fraction_gas(self, fe_elem, att):
        options = ['molar fraction key',]
        self._render_items(fe_elem, att, options)
        # Sub group
        model_params = ['vapor pressure model type',]
        model_params_elem = self._new_list(fe_elem, 'vapor pressure model parameters')
        self._render_items(model_params_elem, att, model_params)

    def render_compressible_porosity(self, fe_elem, att):
        options = ['pressure key', 'base porosity key', 'porosity key']
        self._render_items(fe_elem, att, options)
        # Sub group
        model_params = ['pore compressibility [Pa^-1]',]
        model_params_elem = self._new_list(fe_elem, 'compressible porosity model parameters')
        region_name = att.findComponent('region').value().name()
        region_elem = self._new_list(model_params_elem, region_name)
        self._new_param(region_elem, 'region', 'string', region_name)
        self._render_items(region_elem, att, model_params)

    def render_overland_pressure_water_content(self, fe_elem, att):
        options = ['molar mass', 'allow negative water content', 'water content rollover', 'pressure key', 'cell volume key']
        self._render_items(fe_elem, att, options)

    def render_ponded_depth(self, fe_elem, att):
        options = ['ponded depth bar', 'height key']
        self._render_items(fe_elem, att, options)

    def write(self, xml_root):
        """Perform the XML write out."""
        state_elem = self._new_list(xml_root, 'state')

        #### handle field evaluators
        renderers = {
            'richards water content': self.render_richards_water_content,
            'viscosity': self.render_viscosity,
            'capillary pressure, atmospheric gas over liquid': self.render_capillary_pressure,
            'effective_pressure': self.render_effective_pressure,
            'molar fraction gas': self.render_molar_fraction_gas,
            'compressible porosity': self.render_compressible_porosity,
            'overland pressure water content': self.render_overland_pressure_water_content,
            'ponded depth': self.render_ponded_depth,
        }

        fe_list_elem = self._new_list(state_elem, 'field evaluators')

        basic_templates = {
            "multiplicative evaluator": "fe-multiplicative-evaluator.xml",
        }

        smart_templates = {
            "independent variable": ("fe-independent-variable.xml", map_independent_variable),
            "independent variable - function": ("fe-independent-variable-function.xml", map_independent_variable_function),
            "eos": ("fe-eos.xml", map_eos),
            "eos-constant": ("fe-eos-constant.xml", map_eos_constant),
            "eos-vapor": ("fe-eos-vapor.xml", map_eos_vapor),
        }

        fe_atts = shared.sim_atts.findAttributes('field-evaluator-base')
        for att in fe_atts:
            name = att.name()
            fe_type = att.type()
            if fe_type in basic_templates:
                append_template(fe_list_elem, basic_templates[fe_type], {r"${NAME}": name})
            elif fe_type in smart_templates:
                # We gotta be smart
                fname, func = smart_templates[fe_type]
                mapping = func(att)
                append_template(fe_list_elem, fname, mapping)
            # New implementation!
            elif fe_type in renderers:
                fe_elem = self._new_list(fe_list_elem, name)
                self._new_param(fe_elem, 'field evaluator type', 'string', fe_type)
                renderers[fe_type](fe_elem, att)
            else:
                raise NotImplementedError('Field evaluator `{}` not implemented'.format(fe_type))



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
