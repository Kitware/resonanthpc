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

"""Common base class for writers"""

import os

print("loading", os.path.basename(__file__))

import smtk
import smtk.attribute
import smtk.model

from .shared_data import instance as shared

TypeStringMap = {
    smtk.attribute.Item.DoubleType: "double",
    smtk.attribute.Item.IntType: "int",
    smtk.attribute.Item.StringType: "string",
    smtk.attribute.Item.VoidType: "bool",
    smtk.attribute.Item.FileType: "string",
}

FLOAT_FORMAT = r"{:e}"


class BaseWriter:
    """Base writer class for ATS input files.

    Should ONLY contain methods (no member data)
    """

    def __init__(self):
        """"""
        # Do NOT include any member data
        pass

    def _get_native_model_path(self, resource):
        """"""
        # We only support model resource filenames for now
        model_res = smtk.model.Resource.CastTo(resource)
        if model_res is None:
            return None

        # Unfortunately, this logic is all part of SMTK lore.
        uuids = model_res.entitiesMatchingFlags(smtk.model.MODEL_ENTITY, True)
        if not uuids:
            raise RuntimeError("No model entities in model resource")

        model_uuid = uuids.pop()
        if not model_res.hasStringProperty(model_uuid, "url"):
            raise RuntimeError('Model resource missing "url" property')
        prop_list = model_res.stringProperty(model_uuid, "url")
        return prop_list[0]

    def _new_list(self, parent, list_name, list_type="ParameterList"):
        """Appends ParameterList element to parent

        If list_type is None, then that xml attribute is omitted
        """
        new_list = shared.xml_doc.createElement("ParameterList")
        new_list.setAttribute("name", list_name)
        if list_type is not None:
            new_list.setAttribute("type", list_type)
        parent.appendChild(new_list)
        return new_list

    def _new_param(self, list_elem, param_name, param_type, param_value):
        """Appends Parameter element to list_elem"""
        if not isinstance(param_value, str):
            raise TypeError(
                "trying to insert and invalid value for: ({}: {})".format(
                    param_name, param_value
                )
            )
        new_param = shared.xml_doc.createElement("Parameter")
        new_param.setAttribute("name", param_name)
        new_param.setAttribute("type", param_type)
        new_param.setAttribute("value", param_value)
        list_elem.appendChild(new_param)
        return new_param

    def _render_associations(self, parent_elem, att, elem_name_or_list):
        """Generates Parameter element for attribute associations."""
        ref_item = att.associations()
        if ref_item is None:
            print(
                'Warning: expected attribute "{}" to have associations'.format(
                    att.name()
                )
            )
            return

        n = ref_item.numberOfValues()
        if n == 0:
            print(
                'Warning: expected attribute "{}" to have associations'.format(
                    att.name()
                )
            )
            return

        if isinstance(elem_name_or_list, (list, tuple)) and len(elem_name_or_list) > 1:
            elem_name = elem_name_or_list[0]
            array_name = elem_name_or_list[1]
        else:
            elem_name = elem_name_or_list
            array_name = elem_name

        # Generate list of attribute names
        value_list = list()
        for i in range(n):
            if ref_item.isSet(i):
                value_att = ref_item.value(i)
                value_list.append(value_att.name())

        if len(value_list) == 0:
            print(
                'Warning: expected attribute "{}" to have associations'.format(
                    att.name()
                )
            )
            return

        if len(value_list) == 1:
            self._new_param(parent_elem, elem_name, "string", value_list[0])
            return

        # (else) n > 1
        value_string = ",".join(value_list)
        array_string = "{{{}}}".format(value_string)
        self._new_param(parent_elem, array_name, "Array(string)", array_string)

    def _render_items(
        self, parent_elem, att, param_names, force_array=False, index=None
    ):
        """Generates Parameter elements for items specified by param_names"""
        assert isinstance(param_names, list)
        for param_name in param_names:
            if index is not None:
                item = att.find(index, param_name)
            else:
                item = att.find(param_name)
            if item is None:
                continue

            # TODO: we need to handle `ComponentType`

            # skip over optional items if not enabled. Bools are never optional... weird logic here.
            if item.type() != smtk.attribute.Item.VoidType and not item.isEnabled():
                continue

            type_string = TypeStringMap.get(item.type())
            value = None
            if item.type() == smtk.attribute.Item.VoidType:
                value = "true" if item.isEnabled() else "false"
            elif hasattr(item, "numberOfValues") and (
                force_array or item.numberOfValues() > 1
            ):
                type_string = "Array({})".format(type_string)
                value_list = list()
                for i in range(item.numberOfValues()):
                    value_list.append(item.value(i))
                string_list = [str(x) for x in value_list]
                value = r"{" + ",".join(string_list) + r"}"
            elif hasattr(item, "value"):
                value = str(item.value())
                if isinstance(value, float):
                    value = FLOAT_FORMAT.format(value)
                else:
                    value = str(value)
            else:
                raise NotImplementedError(
                    "({}) for ({}) is not handled".format(item.type(), param_name)
                )

            self._new_param(parent_elem, param_name, type_string, value)
        return

    def _render_io_event_specs(self, parent_elem, io_event):
        extensible_groups = {
            "cycles start period stop": {
                "array": ["Start Cycle", "Cycle Period", "Stop Cycle",],
                "items": [],
            },
            "times start period stop": {
                "array": ["Start Time", "Time Period", "Stop Time",],
                "items": ["units"],  # NOTE: assumes all items are string
            },
            "times": {
                'array': ['times'],
                'items': ['units'],
            }
        }
        sub_items = [
            "cycles",  # Int
        ]
        # add the sub items
        self._render_items(parent_elem, io_event, sub_items)

        # add each array of values
        dbl_type_string = "Array({})".format("double")

        def _get_array_values(group, items, idx=0):
            string_list = [str(group.find(idx, nm).value()) for nm in items]
            values = r"{" + ",".join(string_list) + r"}"
            return values

        for group_name in extensible_groups.keys():
            event_group = io_event.find(group_name)
            if event_group.isEnabled():
                meta = extensible_groups[group_name]
                item_names = meta["items"]
                array_names = meta["array"]

                n = event_group.numberOfGroups()
                if n > 1:
                    for i in range(n):
                        name = group_name + " {}".format(i)
                        values = _get_array_values(event_group, array_names, i)
                        self._new_param(parent_elem, name, dbl_type_string, values)
                        for item in item_names:
                            value = str(event_group.find(i, item).value())
                            self._new_param(
                                parent_elem, name + " " + item, "string", value
                            )
                else:
                    values = _get_array_values(event_group, array_names)
                    self._new_param(parent_elem, group_name, dbl_type_string, values)
                    for item in item_names:
                        value = str(event_group.find(item).value())
                        self._new_param(
                            parent_elem, group_name + " " + item, "string", value
                        )

        # TODO: handle times group (non extensible)

        return

    def _render_function(self, parent_elem, att, name=None, _i=0, _recursive=True):

        if att.numberOfGroups() > 1 and _recursive:
            for i in range(att.numberOfGroups()):
                self._render_function(
                    parent_elem, att, name=None, _i=i, _recursive=False
                )
            return

        def _fetch_subgroup_values(group, name):
            values = []
            for i in range(group.numberOfGroups()):
                v = group.find(i, name, smtk.attribute.SearchStyle.IMMEDIATE)
                values.append(v.value())
            return r"{" + ",".join([FLOAT_FORMAT.format(x) for x in values]) + r"}"

        if name is None:
            name = att.find(_i, "function name").value()

        the_group = self._new_list(parent_elem, name)

        # add region
        regions_comp = att.find(_i, "regions")
        value_list = [
            regions_comp.value(k).name() for k in range(regions_comp.numberOfValues())
        ]
        if len(value_list) == 1:
            self._new_param(the_group, "region", "string", value_list[0])
        else:
            regions = r"{" + ", ".join(value_list) + r"}"
            self._new_param(the_group, "regions", "Array(string)", regions)
        # add components
        component = str(att.find(_i, "components").value())
        if component in ("cell", "face", "boundary_face"):
            self._new_param(the_group, "component", "string", component)
        else:
            components = "{" + component + "}"
            self._new_param(the_group, "components", "Array(string)", components)

        function_sub_elem = self._new_list(the_group, "function")
        params = att.find(_i, "variable type")
        func_type = params.value()
        if func_type == "constant":
            constant_elem = self._new_list(function_sub_elem, "function-constant")
            self._render_items(constant_elem, params, ["value",])
        elif func_type == "function-tabular":
            tabular_elem = self._new_list(function_sub_elem, "function-tabular")
            group = params.find("tabular-data")
            x_values = _fetch_subgroup_values(group, "X")
            y_values = _fetch_subgroup_values(group, "Y")
            self._new_param(tabular_elem, "x values", "Array(double)", x_values)
            self._new_param(tabular_elem, "y values", "Array(double)", y_values)
            forms = params.find("forms")
            values = []
            if forms.find("linear").isEnabled():
                values.append("linear")
            if forms.find("constant").isEnabled():
                values.append("constant")
            if len(values):
                forms_values = r"{" + ",".join([x for x in values]) + r"}"
                self._new_param(tabular_elem, "forms", "Array(string)", forms_values)
        elif func_type == "function-linear":
            linear_elem = self._new_list(function_sub_elem, "function-linear")
            # breakpoint()
            y = params.find("y0").value()
            self._new_param(linear_elem, "y0", "double", FLOAT_FORMAT.format(y))
            group = params.find("linear-data")
            x_values = _fetch_subgroup_values(group, "x0")
            g_values = _fetch_subgroup_values(group, "gradient")
            self._new_param(linear_elem, "x0", "Array(double)", x_values)
            self._new_param(linear_elem, "gradient", "Array(double)", g_values)
        elif func_type == "function-file":
            tabular_elem = self._new_list(function_sub_elem, "function-tabular")
            options = ["file", "x header", "y header"]
            self._render_items(tabular_elem, params, options)
        elif func_type == "initialize from 1D column":
            tabular_elem = self._new_list(function_sub_elem, "initialize from 1D column")
            options = ["file", "z header", "f header", "coordinate orientation"]
            self._render_items(tabular_elem, params, options)
            # surface sideset
            sideset_comp = params.find("surface sideset")
            if sideset_comp is not None:
                self._new_param(tabular_elem, "surface sideset", "string", sideset_comp.value().name())
