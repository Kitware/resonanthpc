"""Use AttributeBuilder to generate attribute resource file from yml specification"""

import argparse
import os
import sys

from utilities.attribute_builder import AttributeBuilder
from utilities.resource_io import ResourceIO

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate attribute resource from yml description')
    parser.add_argument('template_filepath', help='Attribute template filename/path (.sbt)')
    parser.add_argument('yml_filepath', help='YAML file specifying the attributes to generate')
    parser.add_argument('-l', '--less_verbose', action='store_true', help='reduce output dumped to the console')
    parser.add_argument('-o', '--output_filepath', default='attributes.smtk', help='output filename/path (ats_input.xml)')
    # parser.add_argument('-s', '--skip_instances', action='store_true', help='skip initializing instanced attributes')
    parser.add_argument('-y', '--yml_module_path', help='Path to yaml parser library')

    args = parser.parse_args()
    # print(args)

    # Add path to yaml lib
    yml_module_path = args.yml_module_path
    if yml_module_path is None:
        # Default path from the repository
        source_path = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(source_path, os.pardir, os.pardir, os.pardir, 'thirdparty', 'pyyaml', 'lib3')
        yml_module_path = os.path.normpath(path)
    if not os.path.exists(yml_module_path):
        print('WARNING: yml_module_path not found:', yml_module_path)
    else:
        sys.path.insert(0, yml_module_path)

    # Load yml file as the attribute specification
    spec = None
    import yaml
    print('Loading yaml file:', args.yml_filepath)
    with open(args.yml_filepath) as fp:
        content = fp.read()
        spec = yaml.safe_load(content)
    assert spec is not None

    # Initialize ResourceIO and load template
    res_io = ResourceIO()
    att_resource = res_io.import_resource(args.template_filepath)
    assert att_resource is not None

    # Initialize builder and populate the attributes
    verbose = not args.less_verbose
    builder = AttributeBuilder(verbose=verbose)
    builder.build_attributes(att_resource, spec)

    # Write the result
    res_io.write_resource(att_resource, args.output_filepath)
    print('Wrote', args.output_filepath)
