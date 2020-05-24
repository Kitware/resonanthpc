"""
Basic yml format:

# Create attribute (default "action: create")
- type: string  # must be instanced unless name provided
    name: string  # optional but when included has priority over type
    items:
    # Option 1: shorthand for setting value
    - name: float | int | str | list

    # Option 2: for more options
    - name: string
        value: float | int | str | list

# Used "edit" to find and modify existing attribute
- action: edit
  type: string
  name: string  # optional
"""

import smtk
import smtk.attribute
import smtk.model
import smtk.view


class AttributeBuilder:
    """A utility class for generating and populating attribute resources.


    Inputs a formatted object specifying the contents to generate.
    """

    def __init__(self, verbose=False):
        """"""
        self.att_resource = None
        self.model_resource = None
        self.pedigree_lookup = dict()  # <face/volume.pedigree-id, smtk.model.Entity>
        self.spec = None
        self.verbose = verbose

    def build_attributes(self, att_resource, spec, model_resource=None, verbose=None):
        """Create and populate attributes based on input specification.

        Args:
            att_resource: smtk::attribute::Resource
            spec: dict with attribute specfications
            model_resource: smtk::attribute::Model
            verbose: boolean to enable print statements
        """
        assert isinstance(spec, list), 'input spec must be a list, not {}'.format(type(spec))
        self.spec = spec

        if verbose is not None:
            self.verbose = verbose

        self.att_resource = att_resource
        self.model_resource = model_resource
        atts = att_resource.attributes()
        self._post_message('Initial attribute count: {}'.format(len(atts)))

        if model_resource is not None:
            self._build_pedigree_lookup(model_resource)

        # Create instanced attributes first
        self.create_instanced_atts(self.att_resource)

        # Traverse the elements in the input spec
        assert isinstance(spec, list), 'top-level specification be a list not {}'.format(type(spec))
        for element in spec:
            assert isinstance(element, dict), 'top-level element must be a dict not {}'.format(type(element))

            action = element.get('action', 'create')  # default action is to create attribute
            if action == 'create':
                att = self._create_attribute(element)
                assert att is not None, 'failed to create attribute'
                self._edit_attribute(att, element)

            elif action == 'edit':
                att = self._find_attribute(element)
                assert att is not None, 'failed to find attribute'
                self._post_message(
                    'Editing attribute \"{}\"'.format(att.name()))
                self._edit_attribute(att, element)
            else:
                raise RuntimeError('Unrecognized action \"{}\"'.format(action))

        att_count_end = len(att_resource.attributes())
        self._post_message('Final attribute count: {}'.format(att_count_end))

    def create_instanced_atts(self, att_resource):
        """Instantiates all attributes referenced in Instanced views.

        Traverses from top-level view to find all instanced views that
        can potentially be displayed, and creates all instanced attributes.
        """
        top_view = att_resource.findTopLevelView()
        if top_view is None:
            print('WARNING: Attribute resource has no top-level view')
            return

        self._post_message('Generating instanced attributes')
        self._recursive_create_instanced_atts(att_resource, top_view.details())
        instanced_count = len(att_resource.attributes())
        self._post_message(
            'After creating instanced attributes, count: {}'.format(instanced_count))

    def _associate_attribute(self, att, spec):
        """"""
        assert isinstance(spec, list), 'association spec is not a list'
        for element in spec:
            assert isinstance(element, dict), 'association element is not a dict'
            assert len(element.keys()) == 1, 'association element not a single key/value'
            key, value = element.popitem()
            if key == 'attribute':
                ref_name = value
                ref_att = self.att_resource.findAttribute(ref_name)
                assert ref_att is not None, 'attribute with name {} not found'.format(ref_name)
                assert att.associate(ref_att), \
                    'failed to associate attribute {} to {}'.format(ref_name, att.name())
            elif key in ['face', 'volume']:
                lookup_key = '{}.{}'.format(key, value)
                entity = self.pedigree_lookup.get(lookup_key)
                assert entity is not None, 'lookup {} returned None'.format(lookup_key)
                assert att.associate(entity), \
                    'failed to associate entity {} to attribute {}'.format(entity.name(), att.name())
            else:
                raise RuntimeError('Unrecognized association type'.format(key))

    def _build_pedigree_lookup(self, model_resource):
        """Buils a dictionary mapping pedigree id to model entity."""
        self.pedigree_lookup.clear()
        type_info = [ ('face', smtk.model.FACE), ('volume', smtk.model.VOLUME) ]
        for t in type_info:
            prefix, ent_type = t
            uuid_list = model_resource.entitiesMatchingFlags(ent_type, True)
            for uuid in uuid_list:
                if not model_resource.hasIntegerProperty(uuid, 'pedigree id'):
                    continue
                prop_list = model_resource.integerProperty(uuid, 'pedigree id')
                if not prop_list:
                    continue
                ped_id = prop_list[0]
                key = '{}.{}'.format(prefix, ped_id)
                ent = model_resource.findEntity(uuid)
                self.pedigree_lookup[key] = ent

    def _edit_attribute(self, att, spec):
        """Updates attribute as specified.

        Args:
            att: smtk.attribute.Attribute
            spec: dictionary specifying contents
        """
        for key,value in spec.items():
            if key in ['action', 'type', 'name']:
                continue
            elif key == 'items':
                self._edit_items(att, value)
            elif key == 'associate':
                self._associate_attribute(att, value)
            else:
                raise RuntimeError('Unrecognized spec key \"{}\"'.format(key))

    def _edit_items(self, parent, spec):
        """Updates items as specified.

        Args:
            parent: Attribute or GroupItem or ValueItem
            spec: list of item specifications
        """
        assert isinstance(spec, list), 'items spec must be a list, not {}'.format(type(spec))
        for element in spec:
            assert isinstance(element, dict), 'item element spec must be a dict, not {}'.format(type(element))
            value = None
            # Checkfor for name/value shortcut
            if len(element.keys()) == 1:
                name, value = element.popitem()
                # print('name', name, 'value', value, type(value))
            else:
                name = element.get('name')
                value = element.get('value')
            assert name is not None, 'no name found for element'
            assert isinstance(name, str), 'name element must be a string, not {}'.format(type(name))

            # Get the item
            if hasattr(parent, 'findChild'):  # value item
                item = parent.findChild(name, smtk.attribute.SearchStyle.IMMEDIATE_ACTIVE)
            elif hasattr(parent, 'find'):     # attribute or group item
                item = parent.find(name)
            else:
                msg = 'item {} has no find() or findChild() method',format(item.name())
                raise RuntimeError(msg)

            assert item is not None, 'no item with name \"{}\"'.format(name)

            # Apply value if specified
            if value is not None and hasattr(item, 'setValue'):
                if self._is_reference_item(item):
                    self._set_reference_item(item, value)
                elif isinstance(value, (float, int, str)):
                    item.setValue(value)
                elif isinstance(value, list):
                    item.setNumberOfValues(len(value))
                    for i in range(len(value)):
                        item.setValue(i, value[i])

            # Check for enabled flag
            enable_key = element.get('enable')
            if enable_key is not None:
                enable_state = bool(enable_key)
                item.setIsEnabled(enable_state)

            # Check for children item spec
            for key in ['items', 'children']:
                children_spec = element.get(key)
                if children_spec:
                    self._edit_items(item, children_spec)

    def _create_attribute(self, spec):
        """"""
        att_type = spec.get('type')
        assert att_type is not None, 'missing attribute \"type\" specification'

        defn = self.att_resource.findDefinition(att_type)
        assert defn is not None, 'missing att definition {}'.format(att_type)

        # Attribute name is optional
        att_name = spec.get('name')
        if att_name is None:
            att = self.att_resource.createAttribute(defn)
        else:
            att = self.att_resource.createAttribute(att_name, defn)
        assert att is not None, 'failed to create attribute type {}'.format(att_type)
        self._post_message(
            'Created attribute type \"{}\", name \"{}\"'.format(att.type(), att.name()))

        return att

    def _create_instanced_view_atts(self, att_resource, view):
        """Create attributes specified in instanced view.

        """
        comp = view.details()
        atts_comp = comp.child(0)
        for i in range(atts_comp.numberOfChildren()):
            att_comp = atts_comp.child(i)
            att_name = att_comp.attributes().get('Name')
            att_type = att_comp.attributes().get('Type')

            # Attributes can appear in multiple instanced views, so check if
            # att has already been created.
            att = att_resource.findAttribute(att_name)
            if att is not None:
                return

            defn = att_resource.findDefinition(att_type)
            if defn is None:
                raise RuntimeError('Definition {} not found'.format(att_type))
            att = att_resource.createAttribute(att_name, defn)
            # print('Created attribute \"{}\" type \"{}\"').format(att_name, att_type)

    def _find_attribute(self, spec):
        """"""
        # Attribute name is optional, but if specified, takes precedence
        att_name = spec.get('name')
        if att_name is not None:
            att = self.att_resource.findAttribute(att_name)
            return att

        att_type = spec.get('type')
        if att_type is not None:
            att_list = self.att_resource.findAttributes(att_type)
            assert len(att_list) <= 1, 'found multiple attributes of type {}'.format(att_type)
            if att_list:
                return att_list[0]

        # (else)
        return None

    def _is_reference_item(self, item):
        """"""
        return item.type() in [
            smtk.attribute.Item.ComponentType,
            smtk.attribute.Item.ResourceType]

    def _post_message(self, msg):
        """"""
        if self.verbose:
            print(msg)

    def _recursive_create_instanced_atts(self, att_resource, comp):
        """Traverse view components to find/create instanced attributes.

        """
        if comp is None:
            raise RuntimeError('Component is None')

        if comp.name() == 'View':
            title = comp.attributes().get('Title')
            view = att_resource.findView(title)
            if view is None:
                raise RuntimeError('View {} not found'.format(title))

            if view.type() == 'Instanced':
                self._create_instanced_view_atts(att_resource, view)
            else:
                self._recursive_create_instanced_atts(att_resource, view.details())
            return

        # (else) process component children
        for i in range(comp.numberOfChildren()):
            child = comp.child(i)
            self._recursive_create_instanced_atts(att_resource, child)

    def _set_reference_item(self, item, target):
        """Assigns a persistent object (target) to a reference item

        Args:
            item: smtk.attribute.ReferenceItem
            target: either (i)  string for attribute name, or
                           (ii) int for pedigree id

        Note the the target is a HACK to keep things simple.
        """
        if target == 'model':
            # Special case
            assert self.model_resource is not None, 'model resource required to set item {}'.format(item.name())
            assert item.setValue(self.model_resource), 'failed to set model resource on item {}'.format(item.name())
        elif isinstance(target, str):
            target_att = self.att_resource.findAttribute(target)
            assert target_att is not None, 'failed for find attribute with name {}'.format(target)
            assert item.setValue(target_att), 'failed to set reference value {} with attribute {}' \
                .format(item.name(), target)
        elif isinstance(target, int):
            raise NotImplementedError('sorry references to model entities not supportted yet.')
        else:
            raise RuntimeError('Unexpected target type {}. Should be str or int'.format(type(target)))
