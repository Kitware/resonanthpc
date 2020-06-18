#! /bin/sh

alias pysmtk="/Applications/modelbuilder.app/Contents/bin/pvpython"
TEMPLATE="../simulation-workflows/ats/ats.sbt"
BUILDER="../../../smtk-tools/build_attributes.py"
TESTS="../simulation-workflows/ats/internal/tests/"

# Demos 01-04
pysmtk $BUILDER \
  $TEMPLATE \
  "${TESTS}/test_demos/demo.01.yml" \
  -o demo.01.smtk

pysmtk $BUILDER \
  $TEMPLATE \
  "${TESTS}/test_demos/demo.02.yml" \
  -o demo.02.smtk

pysmtk $BUILDER \
  $TEMPLATE \
  "${TESTS}/test_demos/demo.03.yml" \
  -o demo.03.smtk

pysmtk $BUILDER \
  $TEMPLATE \
  "${TESTS}/test_demos/demo.04.yml" \
  -m "${TESTS}/test_demos/att.demo.04.mesh.smtk" \
  -o demo.04.smtk
# NOTE: I put this model file here too


# Rock Creek demo (incomplete!!!!)
pysmtk $BUILDER \
  $TEMPLATE \
  "${TESTS}/test_rock_creek/rock_creek.spinup.homo.yml" \
  -m "${TESTS}/test_rock_creek/att.rock_creek.mesh.smtk" \
  -o rock_creek.smtk
