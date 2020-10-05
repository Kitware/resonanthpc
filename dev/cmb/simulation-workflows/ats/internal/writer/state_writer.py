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

from .shared_data import instance as shared
from .base_writer import BaseWriter, FLOAT_FORMAT


class StateWriter(BaseWriter):
    """Writer for ATS state output lists."""

    def __init__(self):
        super(StateWriter, self).__init__()

    def render_richards_water_content(self, fe_elem, att):
        options = [
            "porosity key",
            "molar density liquid key",
            "saturation liquid key",
            "cell volume key",
        ]
        self._render_items(fe_elem, att, options)

    def render_viscosity(self, fe_elem, att):
        options = [
            "viscosity key",
            "temperature key",
        ]
        self._render_items(fe_elem, att, options)
        # Sub group
        model_params = [
            "viscosity relation type",
        ]
        model_params_elem = self._new_list(fe_elem, "viscosity model parameters")
        self._render_items(model_params_elem, att, model_params)

    def render_capillary_pressure(self, fe_elem, att):
        pass

    def render_effective_pressure(self, fe_elem, att):
        pass

    def render_molar_fraction_gas(self, fe_elem, att):
        options = [
            "molar fraction key",
        ]
        self._render_items(fe_elem, att, options)
        # Sub group
        model_params = [
            "vapor pressure model type",
        ]
        model_params_elem = self._new_list(fe_elem, "vapor pressure model parameters")
        self._render_items(model_params_elem, att, model_params)

    def render_compressible_porosity(self, fe_elem, att):
        options = ["pressure key", "base porosity key", "porosity key"]
        self._render_items(fe_elem, att, options)
        # Sub group
        model_params = [
            "pore compressibility [Pa^-1]",
            "pore compressibility inflection point [Pa^-1]",
        ]
        model_params_elem = self._new_list(
            fe_elem, "compressible porosity model parameters"
        )
        params_group = att.findGroup("compressible porosity model parameters")
        for i in range(params_group.numberOfGroups()):
            region_name = params_group.find(i, "region").value().name()
            name_field = params_group.find(i, "function name")
            name = region_name
            if name_field.isEnabled():
                name = name_field.value()
            region_elem = self._new_list(model_params_elem, name)
            self._new_param(region_elem, "region", "string", region_name)
            self._render_items(region_elem, params_group, model_params, index=i)

    def render_overland_pressure_water_content(self, fe_elem, att):
        options = [
            "molar mass",
            "allow negative water content",
            "water content rollover",
            "pressure key",
            "cell volume key",
        ]
        self._render_items(fe_elem, att, options)

    def render_ponded_depth(self, fe_elem, att):
        options = ["ponded depth bar", "height key"]
        self._render_items(fe_elem, att, options)

    def render_eos(self, fe_elem, att):
        options = ["EOS basis", "molar density key", "mass density key"]
        self._render_items(fe_elem, att, options)
        # Now handle `EOS parameters` parameter list
        params = att.find("EOS type")
        eos_type = params.value()
        params_elem = self._new_list(fe_elem, "EOS parameters")
        self._new_param(params_elem, "EOS type", "string", eos_type)
        if eos_type == "constant":
            key = str(params.find("key").value())
            value = FLOAT_FORMAT.format(params.find("value").value())
            self._new_param(params_elem, key, "double", value)
        elif eos_type == "vapor in gas":
            gas_elem = self._new_list(params_elem, "gas EOS parameters")
            self._new_param(gas_elem, "EOS type", "string", "ideal gas")

    def render_independent_variable(self, fe_elem, att):
        options = [
            "constant in time",
        ]
        self._render_items(fe_elem, att, options)
        function_elem = self._new_list(fe_elem, "function")
        # Function list
        self._render_region_function(function_elem, att.findGroup("function"))

    def _render_dependent_evaluator_base(self, fe_elem, att):
        assocs = att.associations()
        value_list = list()
        for i in range(assocs.numberOfValues()):
            if assocs.isSet(i):
                value_att = assocs.value(i)
                value_list.append(value_att.name())
        linked_fes = r"{" + ", ".join(value_list) + r"}"
        self._new_param(fe_elem, "evaluator dependencies", "Array(string)", linked_fes)

    def render_multiplicative_evaluator(self, fe_elem, att):
        self._render_dependent_evaluator_base(fe_elem, att)
        options = ["coefficient", "enforce positivity"]
        self._render_items(fe_elem, att, options)

    def render_secondary_variable_from_function(self, fe_elem, att):
        self._render_dependent_evaluator_base(fe_elem, att)
        function_elem = self._new_list(fe_elem, "function")
        # Function list
        self._render_function(function_elem, att.find("function"))

    def render_column_sum_evaluator(self, fe_elem, att):
        depends = att.findGroup("evaluator dependency")
        name = depends.find("evaluator").value().name()
        coef_a = depends.find("coefficient")
        self._new_param(fe_elem, "evaluator dependency", "string", name)
        if coef_a.isEnabled():
            self._new_param(fe_elem, name + " coefficient", "double", FLOAT_FORMAT.format(coef_a.value()))

    def render_additive_evaluator(self, fe_elem, att):
        depends = att.findGroup("evaluator dependencies")
        evals = {}
        for i in range(depends.numberOfGroups()):
            name = depends.find(i, "evaluator").value().name()
            coef_a = depends.find(i, "coefficient")
            if coef_a.isEnabled():
                evals[name] = coef_a.value()
            else:
                evals[name] = None
        linked_fes = r"{" + ", ".join(evals.keys()) + r"}"
        self._new_param(fe_elem, "evaluator dependencies", "Array(string)", linked_fes)
        for name, coef in evals.items():
            if coef is not None:
                self._new_param(fe_elem, name + " coefficient", "double", FLOAT_FORMAT.format(coef))

    def render_depth(self, fe_elem, att):
        options = [
            "constant in time",
        ]
        self._render_items(fe_elem, att, options)

    def render_snow_melt_rate(self, fe_elem, att):
        options = [
            "snow melt rate [mm day^-1 C^-1]",
            "snow-ground transition depth [m]",
            "air-snow temperature difference [C]",
        ]
        self._render_items(fe_elem, att, options)

    def render_transpiration_distribution_via_rooting_depth(self, fe_elem, att):
        pass

    def render_potential_evapotranspiration(self, fe_elem, att):
        pass

    def render_rooting_depth_fraction(self, fe_elem, att):
        params_group = att.findGroup("rooting_depth_fraction parameters")
        options = [
            "alpha",
            "beta",
            "max rooting depth [m]",
        ]
        params_elem = self._new_list(fe_elem, "rooting_depth_fraction parameters")
        # TODO: should `broadleaf_deciduous` be able to be changed?
        leaf_elem = self._new_list(params_elem, "broadleaf_deciduous")
        self._render_items(leaf_elem, params_group, options)
        region_name = params_group.find("region").value().name()
        self._new_param(leaf_elem, "region", "string", region_name)

    def render_plant_wilting_factor(self, fe_elem, att):
        params_group = att.findGroup("plant_wilting_factor parameters")
        options = [
            "capillary pressure at fully open stomates [Pa]",
            "capillary pressure at wilting point [Pa]",
        ]
        params_elem = self._new_list(fe_elem, "plant_wilting_factor parameters")
        # TODO: should `broadleaf_deciduous` be able to be changed?
        leaf_elem = self._new_list(params_elem, "broadleaf_deciduous")
        self._render_items(leaf_elem, params_group, options)
        region_name = params_group.find("region").value().name()
        self._new_param(leaf_elem, "region", "string", region_name)

    def write(self, xml_root):
        """Perform the XML write out."""
        state_elem = self._new_list(xml_root, "state")

        #### handle field evaluators
        renderers = {
            "richards water content": self.render_richards_water_content,
            "viscosity": self.render_viscosity,
            "capillary pressure, atmospheric gas over liquid": self.render_capillary_pressure,
            "effective_pressure": self.render_effective_pressure,
            "molar fraction gas": self.render_molar_fraction_gas,
            "compressible porosity": self.render_compressible_porosity,
            "overland pressure water content": self.render_overland_pressure_water_content,
            "ponded depth": self.render_ponded_depth,
            "eos": self.render_eos,
            "independent variable": self.render_independent_variable,
            "multiplicative evaluator": self.render_multiplicative_evaluator,
            "depth": self.render_depth,
            "secondary variable from function": self.render_secondary_variable_from_function,
            "additive evaluator": self.render_additive_evaluator,
            "column sum evaluator": self.render_column_sum_evaluator,
            "snow melt rate": self.render_snow_melt_rate,
            "transpiration distribution via rooting depth": self.render_transpiration_distribution_via_rooting_depth,
            "potential evapotranspiration": self.render_potential_evapotranspiration,
            "rooting depth fraction, one PFT per cell": self.render_rooting_depth_fraction,
            "plant wilting factor": self.render_plant_wilting_factor,
        }

        fe_list_elem = self._new_list(state_elem, "field evaluators")

        fe_atts = shared.sim_atts.findAttributes("field-evaluator")
        for att in fe_atts:
            name = att.name()
            fe_type = att.type()
            if fe_type in renderers:
                fe_elem = self._new_list(fe_list_elem, name)
                self._new_param(fe_elem, "field evaluator type", "string", fe_type)
                renderers[fe_type](fe_elem, att)
            else:
                raise NotImplementedError(
                    "Field evaluator `{}` not implemented".format(fe_type)
                )

        #### handle the initial conditions
        ic_elem = self._new_list(state_elem, "initial conditions")

        known_children = [
            "value",
        ]

        ic_atts = shared.sim_atts.findAttributes("ic-base")
        for att in ic_atts:
            name = att.name()
            ic_list_elem = self._new_list(ic_elem, name)
            self._render_items(ic_list_elem, att, known_children)

        return
