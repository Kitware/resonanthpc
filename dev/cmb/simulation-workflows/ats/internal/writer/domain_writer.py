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

import imp
import os
print('loading', os.path.basename(__file__))
from xml.dom import minidom

import smtk
import smtk.attribute

from .shared_data import instance as shared
from . import base_writer
from .base_writer import BaseWriter


class DomainWriter(BaseWriter):
    """Writer for ATS domain elements."""
    def __init__(self):
        super(DomainWriter, self).__init__()

    def write(self, xml_root):
        """"""
        # Lookup table for mesh type to xml attribute
        mesh_type_params = {
            'mesh.generate': 'generate mesh',
            'mesh.resource': 'read mesh file',
            'mesh.surface': 'surface',
        }

        # Association parameters
        assoc_params = {
            'mesh.surface': ['surface sideset name', 'surface sideset names'],
        }

        # possible children_params parameters
        children_params = {
            'mesh.generate': ['domain low coordinate', 'domain high coordinate', 'number of cells'],
            'mesh.resource': [],
            'mesh.surface': ['export mesh to file', ],
            'subgrid': ['subgrid region name', 'entity kind', 'parent domain', 'flyweight mesh'],
            # TODO: column mesh
        }
        main_param_names = ['verify mesh', 'deformable mesh']

        ####
        # Logic to render the mesh section
        mesh_elem = self._new_list(xml_root, 'mesh')
        domain_atts = shared.sim_atts.findAttributes('mesh')
        for domain_att in domain_atts:
            # Write out each domain (mesh)
            mesh_type = domain_att.type()
            mesh_type_string = mesh_type_params.get(domain_att.type())
            if mesh_type_string is None:
                raise NotImplementedError('Unsupported mesh type', domain_att.type())

            # Create list element
            domain_elem = self._new_list(mesh_elem, domain_att.name())
            _ = self._new_param(domain_elem, 'mesh type', 'string', mesh_type_string)

            # Special cases
            if mesh_type == 'mesh.resource':
                resource_item = domain_att.find('resource')
                resource = resource_item.value()
                if resource is None:
                    raise RuntimeError('Model not loaded for ResourceItem {}'.format(item.name()))
                path = self._get_native_model_path(resource)
                if path is None:
                    raise RuntimeError('Model file not found for ResourceItem {}'.format(item.name()))
                # For now, just write the base filename
                filename = os.path.basename(path)
                self._new_param(domain_elem, 'file', 'string', filename)
                # Todo Extend to include MSTK mesh files
                self._new_param(domain_elem, 'format', 'string', 'Exodus II')

            #  Children params
            gen_params_list_name = '{} parameters'.format(mesh_type_string)
            gen_params_list = self._new_list(domain_elem, gen_params_list_name)

            # Association params
            assoc_params_list = assoc_params.get(mesh_type)
            if assoc_params_list:
                self._render_associations(gen_params_list, domain_att, assoc_params_list)

            # Remaining params
            known_children_params = children_params.get(mesh_type, [])
            self._render_items(gen_params_list, domain_att, known_children_params)
            # TODO: If a `domain` mesh, not a surface or otherwise, add the partitioner option:
            #       there aren't any examples of this being used, so leaving out
            # if domain mesh: # psuedo-code
            #     self._render_items(gen_params_list, type_item, ['partitioner',])
            # Top level mesh parameters
            self._render_items(domain_elem, domain_att, main_param_names)
        return
