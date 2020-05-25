# Build Attributes from Specification

The build_attributes.py script can generate attribute resource files (.smtk)
from a yml input file organized as a list of attribute specifcations.

The script requires a yaml parser, which is not readily available with
pre-built pythons executables that include the SMTK modules. For this reason,
the [PyYAML source repository](https://github.com/yaml/pyyaml) is included as
a submodule at `thirdparty/pyyaml`, and its path is included by default when
the `build_attribues.py` script is run.

Example files are include to generate ATS demos 01 and 04. From the
`resonantrpc/dev/cmb/utilities` folder, . To generate demo attributes:

```bash
alias pysmtk="/Applications/modelbuilder.app/Contents/bin/pvpython"
cd dev/cmb/utilities

pysmtk build_attributes.py ../simulation-workflows/ats/ats.sbt \
  ../simulation-workflows/ats/internal/tests/test_demos/demo.01.yml \
  -o att.demo.01.smtk

pysmtk build_attributes.py ../simulation-workflows/ats/ats.sbt \
  ../simulation-workflows/ats/internal/tests/test_demos/demo.04.yml \
  -m ../simulation-workflows/ats/internal/tests/test_demos/att.demo.04.mesh.smtk \
  -o att.demo.04.smtk
```

Note that the demo04 case includes the open-book model resource as a script
argument.

The yml file format is a work in progress, but is essentially a list of
dictionary objects, with each object specifying one attribute to be created
and/or edited. Check the top of `utilites/attribute_builder.py` for a few
schema notes.


For instanced attributes, be sure to add `action: edit` to the YAML item.
