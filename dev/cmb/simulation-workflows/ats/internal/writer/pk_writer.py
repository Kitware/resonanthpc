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
            "backtrack max total steps",
            "backtrack lag",
            "backtrack factor",
            "backtrack last iterations",
            "backtrack tolerance",
            "backtrack fail on bad search direction",
            "nonlinear tolerance",
            "diverged tolerance",
            "limit iterations",
            "max nka vectors",
            "nka vector tolerance",
            "monitor",
            "max error growth factor",
            "modify correction",
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

            residual_debug = time_int_att.findGroup("ResidualDebugger")
            if residual_debug.isEnabled():
                residual_debug_list = self._new_list(time_int_elem, "ResidualDebugger")
                self._render_items(
                    residual_debug_list, residual_debug, ["cycles"], force_array=True
                )

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
        field = att.find("preconditioner")
        if field.isEnabled():
            prec_att = field.value()
            prec_elem = self._new_list(pk_elem, "preconditioner")
            self._new_param(prec_elem, "preconditioner type", "string", prec_att.type())
            params = self._new_list(prec_elem, prec_att.type() + " parameters")
            self._render_items(params, prec_att, options[prec_att.type()])

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
            criteria = [
                "relative rhs",
                "relative residual",
                "absolute residual",
                "make one iteration",
            ]
            crit_grp = solver.findGroup("convergence criteria")
            criteria_to_add = []
            for crit in criteria:
                if crit_grp.find(crit).isEnabled():
                    criteria_to_add.append(crit)
            if len(criteria_to_add) > 1:
                value = r"{" + ",".join(criteria_to_add) + r"}"
                self._new_param(
                    params_elem, "convergence criteria", "Array(string)", value
                )
            else:
                value = criteria_to_add[0]
                self._new_param(params_elem, "convergence criterial", "string", value)

        return

    def _render_elevation_evaluator(self, pk_elem, att):
        eval_elem = self._new_list(pk_elem, "elevation evaluator")
        ####
        elev_group = att.find("elevation function")
        ef_elem = self._new_list(eval_elem, "elevation function")
        # function
        self._render_region_function(ef_elem, elev_group, "Elevation")
        ####
        slope_group = att.find("slope function")
        sf_elem = self._new_list(eval_elem, "slope function")
        # function
        self._render_region_function(sf_elem, slope_group, "Slope magnitude Left/Right page")
        return

    def _render_overland_conductivity_evaluator(self, pk_elem, att):
        options = ["height key", "slope key", "coefficient key"]
        children = {
            "manning": ["Manning exponent", "slope regularization epsilon"],
            "manning harmonic mean": [
                "Manning exponent",
                "slope regularization epsilon",
            ],
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

    def _render_pk_physical(self, pk_elem, att, render_base=True):
        if render_base:
            self._render_pk_base(pk_elem, att)
        options = [
            "primary variable key",
        ]
        self._render_items(pk_elem, att, options)

        dm_field = att.find("domain name")
        if dm_field.isEnabled():
            dm_nm = dm_field.value().name()
            self._new_param(pk_elem, "domain name", "string", dm_nm)

        debug_group = att.findGroup("debugger")
        for fe in ["debug cells", "debug faces"]:
            item = debug_group.find(fe)
            if item.isEnabled():
                value_list = []
                for i in range(item.numberOfValues()):
                    value_list.append(item.value(i))
                string_list = [str(x) for x in value_list]
                value = r"{" + ",".join(string_list) + r"}"
                self._new_param(pk_elem, fe, "Array(int)", value)
        # render initial condition
        ic_options = [
            "initialize faces from cells",
            "initialize surface head from subsurface",
        ]
        ic_group = att.findGroup("initial condition")
        ic_elem = self._new_list(pk_elem, "initial condition")
        cond_type = ic_group.find("condition type")
        self._render_items(ic_elem, ic_group, ic_options)
        if ic_group.isEnabled() and cond_type.isEnabled():
            if cond_type.value() == "scalar field":
                # Handle function
                func_group = cond_type.find("function")
                cond_name = cond_type.find("condition name").value()
                sub = self._new_list(ic_elem, "function")
                self._render_region_function(sub, func_group, cond_name)
            elif cond_type.value() == "constant scalar":
                # handle scalar value
                value = FLOAT_FORMAT.format(cond_type.find("scalar value").value())
                self._new_param(ic_elem, "value", "double", value)
            elif cond_type.value() == "constant vector 2d":
                raise NotImplementedError()
                # handle vector values
            elif cond_type.value() == "constant vector 3d":
                raise NotImplementedError()
            elif cond_type.value() == "1D column":
                column_elem = self._new_list(ic_elem, "initialize from 1D column")
                options = ["file", "z header", "f header", "coordinate orientation"]
                self._render_items(column_elem, cond_type, options)
                # surface sideset
                sideset_comp = cond_type.find("surface sideset")
                if sideset_comp is not None:
                    self._new_param(column_elem, "surface sideset", "string", sideset_comp.value().name())
            elif cond_type.value() == "restart from file":
                # restart from file
                path = cond_type.find("restart file").value()
                self._new_param(ic_elem, "restart file", "string", path)
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

    def _render_pk_bdf(self, pk_elem, att, render_base=True):
        if render_base:
            self._render_pk_base(pk_elem, att)
        self._generate_time_integrator_section(pk_elem, att)
        self._generate_preconditioner_section(pk_elem, att)
        self._generate_linear_solver(pk_elem, att)
        options = [
            "initial time step",
        ]
        self._render_items(pk_elem, att, options)

    def _render_pk_physical_bdf(self, pk_elem, att):
        self._render_pk_base(pk_elem, att)
        self._render_pk_physical(pk_elem, att, render_base=False)
        self._render_pk_bdf(pk_elem, att, render_base=False)

        options = [
            "conserved quantity key",
        ]
        self._render_items(pk_elem, att, options)

        # diffusion
        diff_group = att.findGroup("diffusion")
        if diff_group.isEnabled():
            diff_options = [
                "discretization primary",
                "gravity",
                "Newton correction",
                "scaled constraint equation",
                "constraint equation scaling cutoff",
                "absolute error tolerance",
            ]
            diff_elem = self._new_list(pk_elem, "diffusion")
            self._render_items(diff_elem, diff_group, diff_options)

        # diffusion preconditioner
        diff_pre_group = att.findGroup("diffusion preconditioner")
        if diff_pre_group.isEnabled():
            diff_pre_options = [
                "Newton correction",
                "include Newton correction",
            ]
            diff_pre_elem = self._new_list(pk_elem, "diffusion preconditioner")
            self._render_items(diff_pre_elem, diff_pre_group, diff_pre_options)

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
        wre_options = ["use surface rel perm", "minimum rel perm cutoff"]
        self._render_items(wre_elem, wre_group, wre_options)
        wre_params = self._new_list(wre_elem, "WRM parameters")
        wrm_options = {
            "van Genuchten": [
                "van Genuchten alpha [Pa^-1]",
                "residual saturation [-]",
                "Mualem exponent l [-]",
                "van Genuchten m [-]",
                "smoothing interval width [saturation]",
                "saturation smoothing interval [Pa]",
            ],
        }
        evaluator = att.findGroup("WRM evaluators")
        for i in range(evaluator.numberOfGroups()):
            region = evaluator.find(i, "region").value().name()
            name_a = evaluator.find(i, "evaluator name")
            if name_a.isEnabled():
                name = name_a.value()
            else:
                name = region
            wrm = evaluator.find(i, "WRM Type")
            wrm_type = wrm.value()
            wre_reg_params = self._new_list(wre_params, name)
            self._new_param(wre_reg_params, "region", "string", region)
            self._new_param(wre_reg_params, "WRM Type", "string", wrm_type)
            self._render_items(wre_reg_params, wrm, wrm_options[wrm_type])

    def _render_pk_richards_steady_state(self, pk_elem, att):
        self._render_pk_richards_flow(pk_elem, att)

    def _render_pk_overland_pressure(self, pk_elem, att):
        self._render_pk_physical_bdf(pk_elem, att)
        options = [
            "imit correction to pressure change [Pa]",
            "limit correction to pressure change when crossing atmospheric [Pa]",
            "allow no negative ponded depths",
            "min ponded depth for velocity calculation",
            "min ponded depth for tidal bc",
        ]
        self._render_items(pk_elem, att, options)

    def _render_pk_coupled_water(self, pk_elem, att):
        subsurf = att.find("subsurface pk").value().name()
        surf = att.find("surface pk").value().name()
        # must be {subsurface_flow_pk, surface_flow_pk}
        order = r"{" + ",".join([subsurf, surf]) + r"}"
        self._new_param(pk_elem, "PKs order", "Array(string)", order)

        options = ["subsurface domain name", "surface domain name"]
        self._render_items(pk_elem, att, options)

        wd_group = att.findGroup("water delegate")
        wd_options = [
            "modify predictor with heuristic",
            "modify predictor damp and cap the water spurt",
            "cap the water spurt",
            "damp the water spurt",
            "damp and cap the water spurt",
            "cap over atmospheric",
        ]
        wd_elem = self._new_list(pk_elem, "water delegate")
        self._render_items(wd_elem, wd_group, wd_options)

        self._render_pk_bdf(pk_elem, att)

        return

    def _render_pk_weak(self, pk_elem, att):
        pks_comp = att.find("PKs")
        value_list = [pks_comp.value(k).name() for k in range(pks_comp.numberOfValues())]
        order = r"{" + ",".join(value_list) + r"}"
        self._new_param(pk_elem, "PKs order", "Array(string)", order)
        self._render_pk_bdf(pk_elem, att)

    def _render_pk_surface_balance(self, pk_elem, att):
        self._render_pk_physical_bdf(pk_elem, att)
        options = ["modify predictor positivity preserving"]
        self._render_items(pk_elem, att, options)

    def write(self, xml_root):
        """Perform the XML write out."""
        pks_elem = self._new_list(xml_root, "PKs")

        renderers = {
            "richards flow": self._render_pk_richards_flow,
            "richards steady state": self._render_pk_richards_steady_state,
            "overland flow, pressure basis": self._render_pk_overland_pressure,
            "coupled water": self._render_pk_coupled_water,
            "weak MPC": self._render_pk_weak,
            "general surface balance": self._render_pk_surface_balance,
        }

        # Fetch the cycle driver to find out which PK is chosen
        coord_inst = shared.sim_atts.findAttribute("cycle driver")
        pk_tree_item = coord_inst.findComponent("PK tree")
        if pk_tree_item is None:
            raise RuntimeError("PK must be selected in the coordinator section.")
        # pk_tree = pk_tree_item.value()

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
