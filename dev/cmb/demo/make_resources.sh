#! /bin/sh
set -e
TEMPLATE="../simulation-workflows/ats/ats.sbt"
BUILDER="../../../smtk-tools/build_attributes.py"
TESTS="../simulation-workflows/tests/"
EXPORTER="../simulation-workflows/export_ats.py"
alias pvpython="/Applications/modelbuilder.app/Contents/bin/pvpython"

# Demos 01-04
mkdir -p demo-01
pvpython $BUILDER \
  $TEMPLATE \
  "${TESTS}/test_demos/demo.01.yml" \
  -o demo-01/demo.01.smtk
pvpython $EXPORTER demo-01/demo.01.smtk -o demo-01/demo.01.xml

mkdir -p demo-02
pvpython $BUILDER \
  $TEMPLATE \
  "${TESTS}/test_demos/demo.02.yml" \
  -o demo-02/demo.02.smtk
pvpython $EXPORTER demo-02/demo.02.smtk -o demo-02/demo.02.xml

mkdir -p demo-03
pvpython $BUILDER \
  $TEMPLATE \
  "${TESTS}/test_demos/demo.03.yml" \
  -o demo-03/demo.03.smtk
pvpython $EXPORTER demo-03/demo.03.smtk -o demo-03/demo.03.xml

mkdir -p demo-04-v
cp ${TESTS}/test_demos/att.demo.04-v.mesh.smtk demo-04-v/
cp ${TESTS}/test_demos/open-book-2D.exo demo-04-v/
pvpython $BUILDER \
  $TEMPLATE \
  "${TESTS}/test_demos/demo.04-v.yml" \
  -m "demo-04-v/att.demo.04-v.mesh.smtk" \
  -o demo-04-v/demo.04-v.smtk
pvpython $EXPORTER demo-04-v/demo.04-v.smtk \
  -o demo-04-v/demo.04-v.xml


# Rock Creek demo (incomplete!!!!)
# pvpython $BUILDER \
#   $TEMPLATE \
#   "${TESTS}/test_rock_creek/rock_creek.spinup.homo.yml" \
#   -m "${TESTS}/test_rock_creek/att.rock_creek.mesh.smtk" \
#   -o rock_creek.smtk
