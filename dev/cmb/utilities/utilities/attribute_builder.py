"""

Basic yml format:

# Update instanced attributes
- instanced: true  # to create instanced attributes

# Modify (existing) attributes
- modify:
    - type: string  # must be instanced unless name provided
      name: string  # optional but when included has priority over type
      items:
        # Option 1: shorthand for setting value
        - name: float | int | str | list

        # Option 2: for more options
        - name: string
          value: float | int | str | list

# Create attributes
- create:
    - type: string
      name: string  # optional

"""

import smtk
import smtk.attribute

from . import instanced_util


class AttributeBuilder:
    """A utility class for generating and populating attribute resources.


    Inputs a formatted object specifying the contents to generate.
    """

    def __init__(self, verbose=False):
        """"""
        self.att_resource = None
        self.spec = None
        self.verbose = verbose

    def build_attributes(self, att_resource, spec, verbose=None):
        """Create and populate attributes based on input specification.

        Args:
            att_resource: smtk::attribute::Resource
            spec: dict with 'instanced' and 'attributes' keys
            verbose: boolean to enable print statements
        """
        assert isinstance(spec, list), 'input spec must be a list, not {}'.format(type(spec))
        self.spec = spec

        if verbose is not None:
            self.verbose = verbose

        self.att_resource = att_resource
        atts = att_resource.attributes()
        self._post_message('Initial attribute count: {}'.format(len(atts)))

        # Traverse the elements in the input spec
        for element in spec:
            assert isinstance(element, dict), 'top-level list item must be dict not {}'.format(type(element))
            assert len(element) == 1, 'top-level dict elements must be length 1 not {}'.format(len(element))

            key, value = element.popitem()
            if key == 'instanced' and bool(value):
                # Create instanced attributes
                self._post_message('Generating instanced attributes')
                instanced_util.create_instanced_atts(self.att_resource)
                instanced_count = len(att_resource.attributes())
                self._post_message(
                    'After creating instanced attributes, count: {}'.format(instanced_count))

            elif key == 'create':
                create_spec = value
                assert isinstance(create_spec, list), 'create spec must be a list, not'.format(type(create_spec))
                for create_element in create_spec:
                    assert isinstance(create_element, dict), \
                        'create element spec must be a dict, not'.format(type(create_element))
                    att = self._create_attribute(create_element)
                    assert att is not None, 'failed to create attribute'
                    self._configure_attribute(att, create_element)

            elif key == 'modify':
                modify_spec = value
                assert isinstance(modify_spec, list), 'modify spec must be a list, not'.format(type(modify_spec))
                for modify_element in modify_spec:
                    assert isinstance(modify_element, dict), 'modify element spec must be a dict, not'.format(type(modify_element))
                    att = self._find_attribute(modify_element)
                    assert att is not None, 'failed to find attribute'
                    self._post_message(
                        'Modifying attribute \"{}\"'.format(att.name()))
                    self._configure_attribute(att, modify_element)

        att_count_end = len(att_resource.attributes())
        self._post_message('Final attribute count: {}'.format(att_count_end))

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
            elif key == 'pedigree':
                raise NotImplementedError('sorry -support for pedigree association is todo')
            else:
                raise RuntimeError('Unrecognized association type'.format(key))

    def _configure_attribute(self, att, spec):
        """Updates attribute contents.

        Args:
            att: smtk.attribute.Attribute
            spec: dictionary specifying contents
        """
        for key,value in spec.items():
            if key in ['type', 'name']:
                continue
            elif key == 'items':
                self._configure_items(att, value)
            elif key == 'associate':
                self._associate_attribute(att, value)
            else:
                raise RuntimeError('Unrecognized spec key \"{}\"'.format(key))

    def _configure_items(self, parent, spec):
        """Process items corresponding to all entries in spec.

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
                    self._configure_items(item, children_spec)

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

    def _set_reference_item(self, item, target):
        """Assigns a persistent object (target) to a reference item

        Args:
            item: smtk.attribute.ReferenceItem
            target: either (i)  string for attribute name, or
                           (ii) int for pedigree id

        Note the the target is a HACK to keep things simple.
        """
        if isinstance(target, str):
            target_att = self.att_resource.findAttribute(target)
            assert target_att is not None, 'failed for find attribute with name {}'.format(target)
            assert item.setValue(target_att), 'failed to set reference value {} with attribute {}' \
                .format(item.name(), target)
        elif isinstance(target, int):
            raise NotImplementedError('sorry references to model entities not supportted yet.')
        else:
            raise RuntimeError('Unexpected target type {}. Should be str or int'.format(type(target)))
