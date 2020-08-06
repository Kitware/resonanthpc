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

import smtk

print("loading", os.path.basename(__file__))

from .shared_data import instance as shared
from .base_writer import BaseWriter, FLOAT_FORMAT


class PKWriter(BaseWriter):
    """Writer for ATS process kernel trees."""

    def __init__(self):
        super(PKWriter, self).__init__()

    def _generate_time_integrator_section(self, parent, att):
        """Generates the XML elements for the time integrator section.

        This is meant to be added to the PK at the top of the tree
        (the one selected by the Coordinator).
        """
        known_children = [
            "extrapolate initial guess",
            "initial time step",
        ]
        nka_bt_ats_children = [
            "nka lag iterations",
            "max backtrack steps",
            "backtrack lag",
            "backtrack factor",
            "backtrack tolerance",
            "nonlinear tolerance",
            "diverged tolerance",
            "limit iterations",
        ]

        controller_children = [
            "max iterations",
            "min iterations",
            "time step reduction factor",
            "time step increase factor",
            "max time step",
            "min time step",
            "growth wait after fail",
            "count before increasing increase factor",
        ]

        time_int = att.find("time integrator")
        if time_int.isEnabled():
            time_int_att = time_int.value()
            time_int_elem = self._new_list(parent, "time integrator")
            self._render_items(time_int_elem, time_int_att, known_children)
            self._new_param(time_int_elem, "solver type", "string", "nka_bt_ats")
            self._new_param(
                time_int_elem, "timestep controller type", "string", "smarter"
            )

            # Verbosity
            verb_list = self._new_list(time_int_elem, "verbosity object")
            self._render_items(verb_list, time_int_att, ["verbosity level"])

            nka_bt_ats_params = self._new_list(time_int_elem, "nka_bt_ats parameters")
            self._render_items(nka_bt_ats_params, time_int_att, nka_bt_ats_children)

            controller_params = self._new_list(
                time_int_elem, "timestep controller smarter parameters"
            )
            self._render_items(controller_params, time_int_att, controller_children)

        return

    def _generate_preconditioner_section(self, pk_elem, att):
        options = {
            "block ilu": [
                "fact: relax value",
                "fact: absolute threshold",
                "fact: relative threshold",
                "fact: level-of-fill",
                "overlap",
                "schwarz: combine mode",
            ],
            "boomer amg": [
                "tolerance",
                "smoother sweeps",
                "cycle applications",
                "strong threshold",
                "relaxation type",
                "coarsen type",
                "max multigrid levels",
                "use block indices",
                "number of functions",
                "nodal strength of connection norm",
                # TODO: verbosity
            ],
            "euclid": [
                "ilu(k) fill level",
                "ilut drop tolerance",
                "rescale row",
                # TODO: verbosity
            ],
        }
        att = att.find("preconditioner").value()
        prec_elem = self._new_list(pk_elem, "preconditioner")
        self._new_param(prec_elem, "preconditioner type", "string", att.type())
        params = self._new_list(prec_elem, att.type() + " parameters")
        self._render_items(params, att, options[att.type()])

    def _render_pk_base(self, pk_elem, att):
        """The base PK class."""
        options = []
        self._render_items(pk_elem, att, options)
        verb_list = self._new_list(pk_elem, "verbose object")
        self._render_items(verb_list, att, ["verbosity level",])

    def _render_pk_base_2(self, pk_elem, att):
        """The base, non-coupler pk class."""
        self._render_pk_base(pk_elem, att)
        options = []
        self._render_items(pk_elem, att, options)
        # render boundary conditions
        bc_function_names = {
            "pressure": "boundary pressure",
            "mass flux": "outward mass flux",
            "seepage face pressure": "boundary pressure",
            "seepage face head": "boundary head",
            "seepage face with infiltration": "outward mass flux",
            "head": "boundary head",
            "fixed level": "fixed level",
            "zero gradient": None,
            "critical depth": None,
        }
        # NOTE: dynamic BCs are not implemented.
        bc_group = att.findGroup("boundary conditions")
        n_bcs = bc_group.numberOfGroups()
        bc_list = self._new_list(pk_elem, "boundary conditions")
        if bc_group.isEnabled():
            # Get number of types of BCs and group each by type
            bc_type_idxs = {}
            for i in range(n_bcs):
                bc_type = bc_group.find(i, "boundary type").value()
                bc_type_idxs.setdefault(bc_type, [])
                bc_type_idxs[bc_type].append(i)
            for bc_type, idxs in bc_type_idxs.items():
                grouping = self._new_list(bc_list, bc_type)
                for i in idxs:
                    this_bc = self._new_list(
                        grouping, bc_group.find(i, "BC name").value()
                    )
                    params = bc_group.find(i, "boundary type")
                    regions_comp = bc_group.find(i, "regions")
                    value_list = [
                        regions_comp.value(k).name()
                        for k in range(regions_comp.numberOfValues())
                    ]
                    regions = r"{" + ", ".join(value_list) + r"}"
                    self._new_param(this_bc, "regions", "Array(string)", regions)
                    func_name = bc_function_names[bc_type]
                    if func_name:
                        params_list = self._new_list(this_bc, func_name)
                        func = self._new_list(params_list, "function-constant")
                        self._new_param(
                            func,
                            "value",
                            "double",
                            FLOAT_FORMAT.format(params.find("BC value").value()),
                        )
        return

    def _render_pk_physical(self, pk_elem, att, render_base=True):
        if render_base:
            self._render_pk_base_2(pk_elem, att)
        options = [
            "primary variable key",
        ]
        self._render_items(pk_elem, att, options)
        debug_group = att.findGroup("debugger")
        self._render_items(pk_elem, debug_group, ["debug cells", "debug faces"])
        # render initial condition
        ic_options = [
            "initialize faces from cells",
        ]
        ic_group = att.findGroup("initial condition")
        ic_elem = self._new_list(pk_elem, "initial condition")
        self._render_items(ic_elem, ic_group, ic_options)
        if ic_group.isEnabled():
            sub = self._new_list(ic_elem, "function")
            subsub = self._new_list(sub, "initial pressure cells")
            # region
            region = ic_group.find("region").value().name()
            self._new_param(subsub, "region", "string", region)
            # components
            components = "{" + str(ic_group.find("components").value()) + "}"
            self._new_param(subsub, "components", "Array(string)", components)
            # The function - NOTE: this is repeated code from field evaluator
            function_sub_elem = self._new_list(subsub, "function")
            params = ic_group.find("variable type")
            func_type = params.value()
            if func_type == "constant":
                constant_elem = self._new_list(function_sub_elem, "function-constant")
                self._render_items(constant_elem, params, ["value",])
            elif func_type == "function":
                tabular_elem = self._new_list(function_sub_elem, "function-tabular")

                group = ic_group.find("tabular-data")

                def _fetch_subgroup_values(group, name):
                    values = []
                    for i in range(group.numberOfGroups()):
                        v = group.find(i, name, smtk.attribute.SearchStyle.IMMEDIATE)
                        values.append(v.value())
                    return values

                x_value_list = _fetch_subgroup_values(group, "X")
                x_value_list = [str(x) for x in x_value_list]
                x_values = r"{" + ",".join(x_value_list) + r"}"

                y_value_list = _fetch_subgroup_values(group, "Y")
                y_value_list = [str(x) for x in y_value_list]
                y_values = r"{" + ",".join(y_value_list) + r"}"

                self._new_param(tabular_elem, "x values", "Array(double)", x_values)
                self._new_param(tabular_elem, "y values", "Array(double)", y_values)

    def _render_pk_bdf(self, pk_elem, att, render_base=True):
        if render_base:
            self._render_pk_base_2(pk_elem, att)
        self._generate_time_integrator_section(pk_elem, att)
        self._generate_preconditioner_section(pk_elem, att)
        pass

    def _render_pk_physical_bdf(self, pk_elem, att):
        self._render_pk_base_2(pk_elem, att)
        self._render_pk_physical(pk_elem, att, render_base=False)
        self._render_pk_bdf(pk_elem, att, render_base=False)
        # TODO: other fields.

    # The above PK renderers should be called internally by the following renderers.

    def _render_pk_richards_flow(self, pk_elem, att):
        self._render_pk_physical_bdf(pk_elem, att)
        options = [
            "permeability type",
            "surface rel perm strategy",
            "relative permeability method",
            "modify predictor with consistent faces",
            "modify predictor for flux BCs",
            "modify predictor via water content",
            "max valid change in saturation in a time step [-]",
            "max valid change in ice saturation in a time step [-]",
            "limit correction to pressure change [Pa]",
            "limit correction to pressure change when crossing atmospheric [Pa]",
            "permeability rescaling",
        ]
        self._render_items(pk_elem, att, options)
        # water retention evaluator specs
        wre_group = att.findGroup("water retention evaluator specs")
        wre_elem = self._new_list(pk_elem, "water retention evaluator")
        wre_params = self._new_list(wre_elem, "WRM parameters")
        wrm_options = [
            "van Genuchten alpha [Pa^-1]",
            "residual saturation [-]",
            "Mualem exponent l [-]",
            "van Genuchten m [-]",
            "smoothing interval width [saturation]",
            "saturation smoothing interval [Pa]",
        ]
        wrm = wre_group.find("WRM Type")
        region = wre_group.find("region").value().name()
        wre_reg_params = self._new_list(wre_params, region)
        self._new_param(wre_reg_params, "region", "string", region)
        self._new_param(wre_reg_params, "WRM Type", "string", wrm.value())
        self._render_items(wre_reg_params, wrm, wrm_options)
        # diffusion
        diff_group = att.findGroup("diffusion")
        diff_options = [
            "discretization primary",
            "gravity",
            "Newton correction",
            "scaled constraint equation",
            "constraint equation scaling cutoff",
        ]
        diff_elem = self._new_list(pk_elem, "diffusion")
        self._render_items(diff_elem, diff_group, diff_options)
        # TODO: source term
        src_group = att.findGroup("source term")
        if src_group.isEnabled():
            src_options = [
                "source",
                "source term is differentiable",
                "explicit source term",
            ]
            self._new_param(pk_elem, "source term", "bool", "true")
            self._render_items(pk_elem, src_group, src_options)

    def _render_pk_richards_steady_state(self, pk_elem, att):
        self._render_pk_richards_flow(pk_elem, att)

    def write(self, xml_root):
        """Perform the XML write out."""
        pks_elem = self._new_list(xml_root, "PKs")

        renderers = {
            "richards flow": self._render_pk_richards_flow,
            "richards steady state": self._render_pk_richards_steady_state,
        }

        # Fetch the cycle driver to find out which PK is chosen
        coord_inst = shared.sim_atts.findAttribute("cycle driver")
        pk_tree_item = coord_inst.findComponent("PK tree")
        if pk_tree_item is None:
            raise RuntimeError("PK must be selected in the coordinator section.")
        pk_tree = pk_tree_item.value()

        pk_atts = shared.sim_atts.findAttributes("pk-base")
        for att in pk_atts:
            name = att.name()
            pk_type = att.type()

            if pk_type not in renderers:
                raise NotImplementedError(f"`{pk_type}` is not implemented yet.")

            pk_elem = self._new_list(pks_elem, name)
            self._new_param(pk_elem, "PK type", "string", pk_type)
            renderers[pk_type](pk_elem, att)

        return
