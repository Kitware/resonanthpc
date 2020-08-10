#! /bin/sh
set -e
alias pysmtk="/Applications/modelbuilder.app/Contents/bin/pvpython"
TEMPLATE="../simulation-workflows/ats/ats.sbt"
BUILDER="../../../smtk-tools/build_attributes.py"
TESTS="../simulation-workflows/ats/internal/tests/"
EXPORTER="../simulation-workflows/export_ats.py"

# Demos 01-04
pysmtk $BUILDER \
  $TEMPLATE \
  "${TESTS}/test_demos/demo.01.yml" \
  -o demo-01/demo.01.smtk
pysmtk $EXPORTER demo-01/demo.01.smtk -o demo-01/demo.01.xml

pysmtk $BUILDER \
  $TEMPLATE \
  "${TESTS}/test_demos/demo.02.yml" \
  -o demo-02/demo.02.smtk
pysmtk $EXPORTER demo-02/demo.02.smtk -o demo-02/demo.02.xml

pysmtk $BUILDER \
  $TEMPLATE \
  "${TESTS}/test_demos/demo.03.yml" \
  -o demo-03/demo.03.smtk
pysmtk $EXPORTER demo-03/demo.03.smtk -o demo-03/demo.03.xml

pysmtk $BUILDER \
  $TEMPLATE \
  "${TESTS}/test_demos/demo.04.yml" \
  -m "${TESTS}/test_demos/att.demo.04.mesh.smtk" \
  -o demo-04/demo.04.smtk
pysmtk $EXPORTER demo-04/demo.04.smtk \
  -o demo-04/demo.04.xml


# Rock Creek demo (incomplete!!!!)
# pysmtk $BUILDER \
#   $TEMPLATE \
#   "${TESTS}/test_rock_creek/rock_creek.spinup.homo.yml" \
#   -m "${TESTS}/test_rock_creek/att.rock_creek.mesh.smtk" \
#   -o rock_creek.smtk
