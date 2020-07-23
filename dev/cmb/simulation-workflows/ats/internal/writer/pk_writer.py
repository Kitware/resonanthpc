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


def map_richards_steady_state_and_2(att):
    bc_assocs = att.associations()
    value_list = list()
    for i in range(bc_assocs.numberOfValues()):
        if bc_assocs.isSet(i):
            value_att = bc_assocs.value(i)
            value_list.append(value_att.name())

    mapping = {
        r"${NAME}": att.name(),
        r"${IC_REGION}": att.findComponent('initial condition').value().name(),
        r"${WRE_REGION}": att.findComponent('water retention evaluator').value().name(),
        r"${BC_REGIONS}": r"{" + ", ".join(value_list) + r"}",
    }
    return mapping


def map_richards_flow_4(att):
    mapping = {
        r"${NAME}": att.name(),
        r"${IC_REGION}": att.findComponent('initial condition').value().name(),
        r"${WRE_REGION}": att.findComponent('water retention evaluator').value().name(),
    }
    return mapping


def map_overland_flow_pressure_basis_4(att):
    mapping = {
        r"${NAME}": att.name(),
    }
    return mapping


def map_overland_flow_pressure_basis_3(att):
    bc_assocs = att.associations()
    value_list = list()
    for i in range(bc_assocs.numberOfValues()):
        if bc_assocs.isSet(i):
            value_att = bc_assocs.value(i)
            value_list.append(value_att.name())

    mapping = {
        r"${NAME}": att.name(),
        r"${IC_REGION}": att.findComponent('initial condition').value().name(),
        r"${ELEV_REGION}": att.findComponent('elevation evaluator').value().name(),
        r"${SLOPE_REGIONS}": r"{" + ", ".join(value_list) + r"}",
    }
    return mapping


def map_overland_flow_pressure_basis_rc_sh(att):
    bc_assocs = att.associations()
    value_list = list()
    for i in range(bc_assocs.numberOfValues()):
        if bc_assocs.isSet(i):
            value_att = bc_assocs.value(i)
            value_list.append(value_att.name())

    mapping = {
        r"${NAME}": att.name(),
        r"${BC_REGIONS}": r"{" + ", ".join(value_list) + r"}",
    }
    return mapping


def map_coupled_water(att):
    mapping = {
        r"${NAME}": att.name(),
        r"${SUBSURFACE_PK}": att.find("subsurface pk").value().name(),
        r"${SURFACE_PK}": att.find("surface pk").value().name(),
    }
    return mapping



class PKWriter(BaseWriter):
    """Writer for ATS process kernel trees."""
    def __init__(self):
        super(PKWriter, self).__init__()


    def _generate_time_integrator_section(self, parent):
        """Generates the XML elements for the time integrator section.

        This is meant to be added to the PK at the top of the tree
        (the one selected by the Coordinator).
        """
        known_children = [
            'extrapolate initial guess',
            'initial time step',
        ]
        nka_bt_ats_children = [
            'nka lag iterations',
            'max backtrack steps',
            'backtrack lag',
            'backtrack factor',
            'backtrack tolerance',
            'nonlinear tolerance',
            'diverged tolerance',
            'limit iterations'
        ]

        controller_children = [
            'max iterations',
            'min iterations',
            'time step reduction factor',
            'time step increase factor',
            'max time step',
            'min time step',
            'growth wait after fail',
            'count before increasing increase factor',
        ]

        time_int_inst = shared.sim_atts.findAttribute('time integrator')
        if time_int_inst is None:
            raise RuntimeError("time integrator is not set")
        time_int_elem = self._new_list(parent, 'time integrator')
        self._render_items(time_int_elem, time_int_inst, known_children)
        self._new_param(time_int_elem, 'solver type', 'string', 'nka_bt_ats')
        self._new_param(time_int_elem, 'timestep controller type', 'string', 'smarter')

        # Verbosity
        verb_list = self._new_list(time_int_elem, 'verbosity object')
        self._render_items(verb_list, time_int_inst, ['verbosity level'])

        nka_bt_ats_params = self._new_list(time_int_elem, 'nka_bt_ats parameters')
        self._render_items(nka_bt_ats_params, time_int_inst, nka_bt_ats_children)

        controller_params = self._new_list(time_int_elem, 'timestep controller smarter parameters')
        self._render_items(controller_params, time_int_inst, controller_children)

        return

    def write(self, xml_root):
        """Perform the XML write out."""
        pks_elem = self._new_list(xml_root, 'PKs')

        smart_templates = {
            "pk-richards": ("pk-richards-steady-state.xml", map_richards_steady_state_and_2),
            "pk-richards-flow-2": ("pk-richards-flow-2.xml", map_richards_steady_state_and_2),
            "pk-richards-flow-4": ("pk-richards-flow-4.xml", map_richards_flow_4),
            "pk-richards-flow-rc-sh": ("pk-richards-flow-rc-sh.xml", map_richards_flow_4),
            "pk-overland-flow-pressure-basis-3": ("pk-overland-flow-pressure-basis-3.xml", map_overland_flow_pressure_basis_3),
            "pk-overland-flow-pressure-basis-4": ("pk-overland-flow-pressure-basis-4.xml", map_overland_flow_pressure_basis_4),
            "pk-overland-flow-pressure-basis-rc-sh": ("pk-overland-flow-pressure-basis-rc-sh.xml", map_overland_flow_pressure_basis_rc_sh),
            "pk-coupled-water": ("pk-coupled-water.xml", map_coupled_water),
            "pk-coupled-water-rc-sh": ("pk-coupled-water-rc-sh.xml", map_coupled_water),
        }

        # Fetch the cycle driver to find out which PK is chosen
        coord_inst = shared.sim_atts.findAttribute('cycle driver')
        pk_tree_item = coord_inst.findComponent('PK tree')
        if pk_tree_item is None:
            raise RuntimeError("PK must be selected in the coordinator section.")
        pk_tree = pk_tree_item.value()

        pk_atts = shared.sim_atts.findAttributes('pk-base')
        for att in pk_atts:
            name = att.name()
            pk_type = att.type()

            if pk_type not in smart_templates:
                raise NotImplementedError(f"`{pk_type}` is not implemented yet.")

            # We gotta be smart
            fname, func = smart_templates[pk_type]
            mapping = func(att)
            # Grab the XML node to add time integrator if needed
            pk_elem = append_template(pks_elem, fname, mapping)

            # Add the cylce driver info
            if att == pk_tree:
                self._generate_time_integrator_section(pk_elem)

        return
