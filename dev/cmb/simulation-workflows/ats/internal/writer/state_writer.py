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

    def render_eos(self, fe_elem, att):
        options = ['EOS basis', 'molar density key', 'mass density key']
        self._render_items(fe_elem, att, options)
        # Now handle `EOS parameters` parameter list
        params = att.find('EOS type')
        eos_type = params.value()
        params_elem = self._new_list(fe_elem, 'EOS parameters')
        self._new_param(params_elem, 'EOS type', 'string', eos_type)
        if eos_type == 'constant':
            key = str(params.find('key').value())
            value = FLOAT_FORMAT.format(params.find('value').value())
            self._new_param(params_elem, key, 'double', value)
        elif eos_type == 'vapor in gas':
            gas_elem = self._new_list(params_elem, 'gas EOS parameters')
            self._new_param(gas_elem, 'EOS type', 'string', 'ideal gas')

    def render_independent_variable(self, fe_elem, att):
        options = ['constant in time',]
        self._render_items(fe_elem, att, options)
        function_elem = self._new_list(fe_elem, 'function')
        domain_elem = self._new_list(function_elem, 'domain')
        # add region
        region = att.findComponent('region').value().name()
        self._new_param(domain_elem, 'region', 'string', region)
        # add components
        components = "{" + str(att.find('components').value()) + "}"
        self._new_param(domain_elem, 'components', 'Array(string)', components)
        # Function list
        function_sub_elem = self._new_list(domain_elem, 'function')
        params = att.find('variable type')
        func_type = params.value()
        if func_type == 'constant':
            constant_elem = self._new_list(function_sub_elem, 'function-constant')
            self._render_items(constant_elem, params, ['value',])
        elif func_type == 'function':
            tabular_elem = self._new_list(function_sub_elem, 'function-tabular')

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

            self._new_param(tabular_elem, 'x values', 'Array(double)', x_values)
            self._new_param(tabular_elem, 'y values', 'Array(double)', y_values)

            self._new_param(tabular_elem, 'forms', 'Array(string)', r'{constant}')

    def render_multiplicative_evaluator(self, fe_elem, att):
        options = ['coefficient', 'enforce positivity']
        self._render_items(fe_elem, att, options)
        assocs = att.associations()
        value_list = list()
        for i in range(assocs.numberOfValues()):
            if assocs.isSet(i):
                value_att = assocs.value(i)
                value_list.append(value_att.name())
        linked_fes = r"{" + ", ".join(value_list) + r"}"
        self._new_param(fe_elem, 'evaluator dependencies', 'Array(string)', linked_fes)

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
            'eos': self.render_eos,
            'independent variable': self.render_independent_variable,
            'multiplicative evaluator': self.render_multiplicative_evaluator,
        }

        fe_list_elem = self._new_list(state_elem, 'field evaluators')

        fe_atts = shared.sim_atts.findAttributes('field-evaluator')
        for att in fe_atts:
            name = att.name()
            fe_type = att.type()
            if fe_type in renderers:
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
