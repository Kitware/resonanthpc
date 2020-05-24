# Build Attributes from Specification

The build_attributes.py script can generate attribute resource files (.smtk)
from a yml input file organized as a list of attribute specifcations.

The script requires a yaml parser, which is not readily available with
pre-built pythons executables that include the SMTK modules. For this reason,
the [PyYAML source repository](https://github.com/yaml/pyyaml) is included as
a submodule at `thirdparty/pyyaml`, and its path is included by default when
the `build_attribues.py` script is run.

Example files are include to generate ATS demos 01 and 04. From the
`resonantrpc/dev/cmb/utilities` folder, . To generate demo01 attributes:

    # cd .../resonantrpc/dev/cmb/utilities
    .../pvpython build_attributes.py \
      ../simulation-workflows/ats/ats.sbt  \
      demo01.yml \
      -o attributes.demo01.smtk

To generate demo04 attributes,

    # cd .../resonantrpc/dev/cmb/utilities
    .../pvpython build_attributes.py \
      ../simulation-workflows/ats/ats.sbt  \
      demo04.yml \
      -m ../simulation-workflows/ats/internal/tests/data/model.open-book-2D.smtk \
      -o attributes.demo04.smtk

Note that the demo04 case includes the open-book model resource as a script
argument.

The yml file format is a work in progress, but is essentially a list of
dictionary objects, with each object specifying one attribute to be created
and/or edited. Check the top of `utilites/attribute_builder.py` for a few
schema notes.
