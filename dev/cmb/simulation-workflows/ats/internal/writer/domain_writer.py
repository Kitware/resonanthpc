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


class DomainWriter(BaseWriter):
    """Writer for ATS mesh/domain elements."""
    def __init__(self):
        super(DomainWriter, self).__init__()

    def write(self, xml_root):
        """"""
        mesh_atts = shared.sim_atts.findAttributes('mesh-base')

        # Render the mesh elements
        mesh_list_elem = self._new_list(xml_root, 'mesh')
        domains = 0
        for mesh_att in mesh_atts:
            if mesh_att.name() == "domain": domains += 1
            self._write_mesh_elem(mesh_list_elem, mesh_att)
        if domains != 1:
            raise RuntimeError("You must have one and only one mesh called `domain`.")

    def _write_mesh_elem(self, parent_elem, mesh_att, domain_att=None):
        """"""
        # Lookup table for mesh type to xml attribute
        mesh_type_params = {
            'mesh.generate': 'generate mesh',
            'mesh.resource': 'read mesh file',
            'mesh.surface': 'surface',
            'mesh.aliased': 'aliased',
        }

        # Association parameters
        assoc_params = {
            'mesh.surface': ['surface sideset name', 'surface sideset names'],
        }

        # possible children_params parameters
        children_params = {
            'mesh.generate': ['domain low coordinate', 'domain high coordinate', 'number of cells'],
            # 'mesh.resource': [],
            'mesh.surface': ['export mesh to file', ],
            'subgrid': ['subgrid region name', 'entity kind', 'parent domain', 'flyweight mesh'],
            # TODO: column mesh
        }
        main_param_names = ['verify mesh', 'deformable mesh']

        mesh_type = mesh_att.type()
        mesh_type_string = mesh_type_params.get(mesh_att.type())
        if mesh_type_string is None:
            raise NotImplementedError('Unsupported mesh type', mesh_att.type())

        # Create list element
        name = mesh_att.name()
        mesh_elem = self._new_list(parent_elem, name)
        _ = self._new_param(mesh_elem, 'mesh type', 'string', mesh_type_string)

        # Special cases
        if mesh_type == 'mesh.resource':
            resource_item = mesh_att.find('resource')
            resource = resource_item.value()
            if resource is None:
                raise RuntimeError('Model not loaded for ResourceItem {}'.format(item.name()))
            path = self._get_native_model_path(resource)
            if path is None:
                raise RuntimeError('Model file not found for ResourceItem {}'.format(item.name()))
            # For now, just write the base filename
            filename = os.path.basename(path)
            file_params_elem = self._new_list(mesh_elem, "read mesh file parameters")
            self._new_param(file_params_elem, 'file', 'string', filename)
            # Todo Extend to include MSTK mesh files
            self._new_param(file_params_elem, 'format', 'string', 'Exodus II')
        elif mesh_type == 'mesh.aliased':
            alias_params = self._new_list(mesh_elem, 'aliased parameters')
            comp = mesh_att.find('alias')
            alias_name = comp.value().name()
            self._new_param(alias_params, 'alias', 'string', alias_name)
        else:
            #  Children params
            gen_params_list_name = '{} parameters'.format(mesh_type_string)
            gen_params_list = self._new_list(mesh_elem, gen_params_list_name)

            # Association params
            assoc_params_list = assoc_params.get(mesh_type)
            if assoc_params_list:
                self._render_associations(gen_params_list, mesh_att, assoc_params_list)

            # Type-specific mesh parameters
            known_children_params = children_params.get(mesh_type, [])
            self._render_items(gen_params_list, mesh_att, known_children_params)

        # Common mesh parameters
        self._render_items(mesh_elem, mesh_att, main_param_names)

        # Domain mesh parameters
        if domain_att is not None:
            self._render_items(mesh_elem, domain_att, ['partitioner'])
