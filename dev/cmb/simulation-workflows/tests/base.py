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
ats_path = os.path.join(source_path, os.pardir, "ats")

TEMPLATE_FILEPATH = os.path.join(ats_path, "ats.sbt")

top_dir = os.path.join(
    source_path, os.pardir, os.pardir, os.pardir, os.pardir,
)
path = os.path.join(top_dir, "smtk-tools",)
utilities_module_path = os.path.normpath(path)
sys.path.insert(0, utilities_module_path)
path = os.path.join(top_dir, "xmltodict",)
utilities_module_path = os.path.normpath(path)
sys.path.insert(0, utilities_module_path)
import yaml
import xmltodict
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
            print("Loading model resource file:", model_path)
            self.model_resource = self.res_io.read_resource(model_path)
            assert (
                self.model_resource is not None
            ), "failed to load model resource from file {}".format(model_path)
        self.att_resource = self.res_io.read_sbt_file(TEMPLATE_FILEPATH)
        assert (
            self.att_resource is not None
        ), "failed to import attribute template from {}".format(TEMPLATE_FILEPATH)

        # Associate the model resource
        if self.model_resource is not None:
            self.att_resource.associate(self.model_resource)

        # Initialize builder and populate the attributes
        self.builder = AttributeBuilder()
        self.builder.build_attributes(
            self.att_resource, spec, model_resource=self.model_resource
        )
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
        if hasattr(self, "res_io"):
            del self.res_io
        if hasattr(self, "builder"):
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

        baseline = xmltodict.parse(baseline_string)
        testing = xmltodict.parse(xml_string)

        def find_index_with_pair(lst, k, v):
            for i, e in enumerate(lst):
                if k in e and e[k] == v:
                    return i
            raise ValueError("Key/Value pair ({}: {}) not found".format(k, v))

        def compare_dict(a, b, parent=""):
            """ensures all key/values in a are in b but not the other way around"""
            for k, va in a.items():
                try:
                    vb = b[k]
                except KeyError as err:
                    try:
                        raise ValueError(
                            "Heirarchy mismatch (key: `{}`, `{}`) under: {}".format(
                                k, a["@name"], parent
                            )
                        )
                    except KeyError:
                        raise err
                if isinstance(va, list) and isinstance(vb, dict):
                    vb = [
                        vb,
                    ]
                if isinstance(va, dict) and isinstance(vb, list):
                    va = [
                        va,
                    ]
                # Do the comparsion recursively
                if isinstance(va, dict):
                    compare_dict(va, vb, parent="->".join([parent, va["@name"]]))
                elif isinstance(va, list):
                    for e in va:
                        try:
                            idx = find_index_with_pair(vb, "@name", e["@name"])
                        except ValueError:
                            raise ValueError(
                                "Parameter ({}) not found".format(e["@name"])
                                + " for "
                                + parent
                            )
                        compare_dict(e, vb[idx], parent="->".join([parent, e["@name"]]))
                else:
                    if k == "@value" and a["@type"] == "double":
                        va = float(va)
                        vb = float(vb)
                    elif k == "@value" and a["@type"] == "Array(double)":
                        # three decimals places is good enough for me
                        va = [round(float(s), 3) for s in va[1:-1].split(",")]
                        vb = [round(float(s), 3) for s in vb[1:-1].split(",")]
                    # do the comparison
                    if va != vb:
                        raise ValueError(
                            "Data mismatch for: {}: ({} != {})".format(parent, va, vb)
                        )
            return True

        self.assertTrue(compare_dict(baseline, testing))
        return
