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

from . import shared
from . import base_writer
from .base_writer import BaseWriter


class DomainWriter(BaseWriter):
    """Writer for ATS domain elements."""
    def __init__(self):
        super(DomainWriter, self).__init__()

    def write(self, xml_root):
        # possible children parameters
        children = {
            'generate mesh': ['domain low coordinate', 'domain high coordinate', 'number of cells'],
            'read mesh file': ['file', 'format'],
            'surface': ['urface sideset name', 'export mesh to file', ], # TODO: more
            'subgrid': ['subgrid region name', 'entity kind', 'parent domain', 'flyweight mesh'],
            # TODO: column mesh
        }
        main_param_names = ['verify mesh', 'deformable mesh']
        # Note about `'partitioner'`: it only makes sense on the "domain" mesh
        ####
        # Logic to render the mesh section
        mesh_elem = self._new_list(xml_root, 'mesh')
        domain_atts = shared.sim_atts.findAttributes('domain')
        for domain_att in domain_atts:
            # save out each domain
            domain_elem = self._new_list(mesh_elem, domain_att.name())
            type_item = domain_att.findString('mesh type')
            mesh_type = type_item.value()
            _ = self._new_param(domain_elem, 'mesh type', 'string', mesh_type)
            #  Winging it here to generate the parameters list
            gen_params_list_name = '{} parameters'.format(mesh_type)
            gen_params_list = self._new_list(domain_elem, gen_params_list_name)
            known_children = children.get(mesh_type, [])
            self._render_items(gen_params_list, type_item, known_children)
            # TODO: If a `domain` mesh, not a surface or otherwise, add the partitioner option:
            #       there aren't any examples of this being used, so leaving out
            # if domain mesh: # psuedo-code
            #     self._render_items(gen_params_list, type_item, ['partitioner',])
            # Top level mesh parameters
            self._render_items(domain_elem, domain_att, main_param_names)
        return
