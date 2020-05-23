"""

Basic yml format:

# Update instanced attributes
instanced:
    - type: string
      name: string  # optional but when included has priority over type
      items:
        # Option 1: shorthand for only setting value
        - name: float | int | str | list

        # Option 2: for more options
        - name: string
          value: float | int | str | list

# Create and update attributes
attributes:
    - type: string
      name: string  # optional

"""

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
        assert isinstance(spec, dict), 'spec is type {}'.format(type(spec))
        self.spec = spec

        if verbose is not None:
            self.verbose = verbose

        self.att_resource = att_resource
        atts = att_resource.attributes()
        self._post_message('Initial attribute count: {}'.format(len(atts)))

        # Build instanced attributes
        instanced_list = spec.get('instanced')
        if instanced_list is not None:
            assert isinstance(instanced_list, list)

            # Create instanced attributes
            self._post_message('Generating instanced attributes')
            instanced_util.create_instanced_atts(self.att_resource)
            instanced_count = len(att_resource.attributes())
            self._post_message(
                'After creating instanced attributes, count: {}'.format(instanced_count))

            # Update instanced attributes
            for entry in instanced_list:
                assert isinstance(entry, dict)
                att = self._find_instance(entry)
                assert att is not None
                self.configure_attribute(att, entry)

        # Build attributes
        attributes_list = spec.get('attributes')
        if attributes_list:
            assert isinstance(attributes_list, list)
            for entry in attributes_list:
                assert isinstance(entry, dict)
                att = self._create_attribute(entry)
                assert att is not None
                self._configure_attribute(att, entry)

        # Todo connect attribute associations
        # Todo connect ReferenceItem values

        att_count_end = len(att_resource.attributes())
        self._post_message('Final attribute count: {}'.format(att_count_end))

    def _configure_attribute(self, att, spec):
        """"""
        for key,value in spec.items():
            if key in ['type', 'name']:
                continue
            elif key == 'items':
                self._configure_items(att, value)
            else:
                raise RuntimeError('Unrecognized spec key \"{}\"'.format(key))

    def _configure_items(self, parent, spec):
        """Process items corresponding to all entries in spec.

        Args:
            parent: Attribute or GroupItem or ValueItem
            spec: list of item specifications
        """
        assert isinstance(spec, list)
        for entry in spec:
            assert isinstance(entry, dict)
            value = None
            # Checkfor for name/value shortcut
            if len(entry.keys()) == 1:
                name, value = entry.popitem()
                # print('name', name, 'value', value, type(value))
            else:
                name = entry.get('name')
                value = entry.get('value')
            assert name is not None
            assert isinstance(name, str)

            item = parent.find(name)
            assert item is not None

            if value is not None and hasattr(item, 'setValue'):
                if isinstance(value, (float, int, str)):
                    item.setValue(value)
                elif isinstance(value, list):
                    item.setNumberOfValues(len(value))
                    for i in range(len(value)):
                        item.setValue(i, value[i])


    def _create_attribute(self, spec):
        """"""
        att_type = spec.get('type')
        assert att_type is not None

        defn = self.att_resource.findDefinition(att_type)
        assert defn is not None

        # Attribute name is optional
        att_name = spec.get('name')
        if att_name is None:
            att = self.att_resource.createAttribute(defn)
        else:
            att = self.att_resource.createAttribute(att_name, defn)
        assert att is not None
        self._post_message(
            'Created attribute type \"{}\", name \"{}\"'.format(att.type(), att.name()))

        return att

    def _find_instance(self, spec):
        """"""
        # Attribute name is optional, but if specified, takes precedence
        att_name = spec.get('name')
        if att_name is not None:
            att = self.att_resource.findAttribute(att_name)
            return att

        att_type = spec.get('type')
        if att_type is not None:
            att_list = self.att_resource.findAttributes(att_type)
            assert len(att_list) <= 1
            if att_list:
                return att_list[0]

        # (else)
        return None

    def _post_message(self, msg):
        """"""
        if self.verbose:
            print(msg)
