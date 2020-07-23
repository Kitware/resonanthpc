import os
import sys
import unittest

import smtk
import smtk.attribute
import smtk.io
import smtk.operation
import smtk.resource
import smtk.session.vtk

from writer import ats_writer

source_path = os.path.abspath(os.path.dirname(__file__))

TEMPLATE_FILEPATH = os.path.join(source_path, os.pardir, os.pardir, 'ats.sbt')


path = os.path.join(source_path, os.pardir, os.pardir, os.pardir, os.pardir, os.pardir, os.pardir, 'smtk-tools')
utilities_module_path = os.path.normpath(path)
sys.path.insert(0, utilities_module_path)
import yaml
from smtk_tools.attribute_builder import AttributeBuilder
from smtk_tools.resource_io import ResourceIO


OPERATION_SUCCEEDED = int(smtk.operation.Operation.SUCCEEDED)  # 3


class BaseTestCase(unittest.TestCase):
    """A Base test case class to handle SMTK manager stuff."""

    def _load_yaml_resource(self,):
        yml_path = os.path.join(self.SOURCE_DIR, self.YAML_RESOURCE)
        with open(yml_path) as fp:
            content = fp.read()
            spec = yaml.safe_load(content)
        assert spec is not None

        # Initialize ResourceIO and load resources
        self.model_resource = None
        self.res_io = ResourceIO()
        if hasattr(self, "MODEL_RESOURCE_FILENAME"):
            model_path = os.path.join(self.SOURCE_DIR, self.MODEL_RESOURCE_FILENAME)
            print('Loading model resource file:', model_path)
            self.model_resource = self.res_io.read_resource(model_path)
            assert self.model_resource is not None, 'failed to load model resource from file {}'.format(model_path)
        self.att_resource = self.res_io.read_sbt_file(TEMPLATE_FILEPATH)
        assert self.att_resource is not None, 'failed to import attribute template from {}'.format(TEMPLATE_FILEPATH)

        # Associate the model resource
        if self.model_resource is not None:
            self.att_resource.associate(self.model_resource)

        # Initialize builder and populate the attributes
        self.builder = AttributeBuilder()
        self.builder.build_attributes(self.att_resource, spec, model_resource=self.model_resource)
        return

    def setUp(self):
        self.att_resource = None
        self.model_resource = None

        self._load_yaml_resource()

        # Initialize writer
        self.writer = ats_writer.ATSWriter(self.att_resource)
        self.writer.setup_xml_root()

    def tearDown(self):
        self.att_resource = None
        self.model_resource = None
        if hasattr(self, 'res_io'):
            del self.res_io
        if hasattr(self, 'builder'):
            del self.builder

    def _read_baseline(self, baseline_path):
        """A helper in case we want to change how we read the XML."""
        with open(baseline_path) as fp:
            baseline_string = fp.read()
        return baseline_string

    def _compare_xml_content(self, xml_string, dump=False):
        """A helper in case we want to get fancier in how we compare the XML."""
        baseline_path = os.path.join(self.SOURCE_DIR, self.BASELINE_XML_FILENAME)
        baseline_string = self._read_baseline(baseline_path)
        if dump:
            with open(os.path.join(self.SOURCE_DIR, "foo.xml"), "w") as f:
                f.write(xml_string)
        self.assertEqual(xml_string, baseline_string)
        return
