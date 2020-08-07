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

    def _generate_linear_solver(self, pk_elem, att):
        options = {
            "gmres": [
                "error tolerance",
                "maximum number of iterations",
                "overflow tolerance",
                "size of Krylov space",
                "controller training start",
                "controller training end",
                "maximum size of deflation space",
                "convergence criterial",
                "preconditioning strategy",
            ],
        }
        field = att.find("linear solver")
        if field.isEnabled():
            solver = field.value()
            stype = solver.type()
            solver_elem = self._new_list(pk_elem, "linear solver")
            self._new_param(solver_elem, "iterative method", "string", stype)
            params_elem = self._new_list(solver_elem, stype + " parameters")
            self._render_items(params_elem, solver, options[stype])
        return

    def _render_elevation_evaluator(self, pk_elem, att):
        eval_elem = self._new_list(pk_elem, "elevation evaluator")
        ####
        elev_group = att.find("elevation function")
        ef_elem = self._new_list(eval_elem, "elevation function")
        e_elem = self._new_list(ef_elem, "Elevation")
        # region
        regions_comp = elev_group.find("regions")
        value_list = [
            regions_comp.value(k).name() for k in range(regions_comp.numberOfValues())
        ]
        regions = r"{" + ", ".join(value_list) + r"}"
        self._new_param(e_elem, "regions", "Array(string)", regions)
        # components
        components = "{" + str(elev_group.find("components").value()) + "}"
        self._new_param(e_elem, "components", "Array(string)", components)
        # function
        self._render_function(e_elem, elev_group)
        ####
        slope_group = att.find("slope function")
        sf_elem = self._new_list(eval_elem, "slope function")
        s_elem = self._new_list(sf_elem, "Slope magnitude Left/Right page")
        # region
        regions_comp = slope_group.find("regions")
        value_list = [
            regions_comp.value(k).name() for k in range(regions_comp.numberOfValues())
        ]
        regions = r"{" + ", ".join(value_list) + r"}"
        self._new_param(s_elem, "regions", "Array(string)", regions)
        # components
        components = "{" + str(slope_group.find("components").value()) + "}"
        self._new_param(s_elem, "components", "Array(string)", components)
        # function
        self._render_function(s_elem, slope_group)
        return

    def _render_overland_conductivity_evaluator(self, pk_elem, att):
        options = ["height key", "slope key", "coefficient key"]
        children = {
            "manning": ["Manning exponent", "slope regularization epsilon"],
        }
        eval_elem = self._new_list(pk_elem, "overland conductivity evaluator")
        self._render_items(eval_elem, att, options)
        model_elem = self._new_list(eval_elem, "overland conductivity model")
        ctype = att.find("overland conductivity type").value()
        self._new_param(model_elem, "overland conductivity type", "string", ctype)
        self._render_items(model_elem, att, children[ctype])
        return

    def _generate_pk_evaluators(self, pk_elem, att):
        field = att.find("evaluators")
        if not field.isEnabled():
            return
        evaluator_renderers = {
            "overland conductivity evaluator": self._render_overland_conductivity_evaluator,
            "elevation evaluator": self._render_elevation_evaluator,
        }
        n = field.numberOfValues()
        # TODO: only one of each type can be used?
        for i in range(n):
            # render each evaluator
            eval = field.value(i)
            etype = eval.type()
            if etype not in evaluator_renderers:
                raise KeyError("Evaluator `{}` not yet implemented.".format(etype))
            evaluator_renderers[etype](pk_elem, eval)
        return

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
        self._generate_pk_evaluators(pk_elem, att)
        return

    def _render_pk_physical(self, pk_elem, att, render_base=True):
        if render_base:
            self._render_pk_base_2(pk_elem, att)
        options = [
            "primary variable key",
        ]
        self._render_items(pk_elem, att, options)

        dm_field = att.find("domain name")
        if dm_field.isEnabled():
            dm_nm = dm_field.value().name()
            self._new_param(pk_elem, "domain name", "string", dm_nm)

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
            cond_name = ic_group.find("condition name").value()
            subsub = self._new_list(sub, cond_name)
            # region
            region = ic_group.find("region").value().name()
            self._new_param(subsub, "region", "string", region)
            # components
            components = "{" + str(ic_group.find("components").value()) + "}"
            self._new_param(subsub, "components", "Array(string)", components)
            self._render_function(subsub, ic_group)

    def _render_pk_bdf(self, pk_elem, att, render_base=True):
        if render_base:
            self._render_pk_base_2(pk_elem, att)
        self._generate_time_integrator_section(pk_elem, att)
        self._generate_preconditioner_section(pk_elem, att)
        options = [
            "initial time step",
        ]
        self._render_items(pk_elem, att, options)

    def _render_pk_physical_bdf(self, pk_elem, att):
        self._render_pk_base_2(pk_elem, att)
        self._render_pk_physical(pk_elem, att, render_base=False)
        self._render_pk_bdf(pk_elem, att, render_base=False)
        self._generate_linear_solver(pk_elem, att)

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

        # source term
        src_group = att.findGroup("source term")
        if src_group.isEnabled():
            src_options = [
                "source key",
                "source term is differentiable",
                "mass source in meters",
                "explicit source term",
            ]
            self._new_param(pk_elem, "source term", "bool", "true")
            self._render_items(pk_elem, src_group, src_options)

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

    def _render_pk_richards_steady_state(self, pk_elem, att):
        self._render_pk_richards_flow(pk_elem, att)

    def _render_pk_overland_pressure(self, pk_elem, att):
        self._render_pk_physical_bdf(pk_elem, att)
        options = [
            "absolute error tolerance",
            "imit correction to pressure change [Pa]",
            "limit correction to pressure change when crossing atmospheric [Pa]",
            "allow no negative ponded depths",
            "min ponded depth for velocity calculation",
            "min ponded depth for tidal bc",
        ]
        self._render_items(pk_elem, att, options)

    def write(self, xml_root):
        """Perform the XML write out."""
        pks_elem = self._new_list(xml_root, "PKs")

        renderers = {
            "richards flow": self._render_pk_richards_flow,
            "richards steady state": self._render_pk_richards_steady_state,
            "overland flow, pressure basis": self._render_pk_overland_pressure,
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
