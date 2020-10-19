#! /bin/sh
set -e
TEMPLATE="../simulation-workflows/ats/ats.sbt"
BUILDER="../../../smtk-tools/build_attributes.py"
TESTS="../simulation-workflows/tests/"
EXPORTER="../simulation-workflows/export_ats.py"

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
cp ${TESTS}/test_demos/mesh.04_v.smtk demo-04-v/
cp ${TESTS}/test_demos/open-book-2D.exo demo-04-v/
pvpython $BUILDER \
  $TEMPLATE \
  "${TESTS}/test_demos/demo.04_v.yml" \
  -m "demo-04-v/mesh.04_v.smtk" \
  -o demo-04-v/demo.04_v.smtk
pvpython $EXPORTER demo-04-v/demo.04_v.smtk \
  -o demo-04-v/demo.04_v.xml

mkdir -p demo-04-superslab
cp ${TESTS}/test_demos/mesh.04_super_slab.smtk demo-04-superslab/
cp ${TESTS}/test_demos/super_slab.exo demo-04-superslab/
pvpython $BUILDER \
  $TEMPLATE \
  "${TESTS}/test_demos/demo.04_super_slab.yml" \
  -m "demo-04-superslab/mesh.04_super_slab.smtk" \
  -o demo-04-superslab/demo.04_super_slab.smtk
pvpython $EXPORTER demo-04-superslab/demo.04_super_slab.smtk \
  -o demo-04-superslab/demo.04_super_slab.xml


mkdir -p demo-05-spinup-gi
cp ${TESTS}/test_demos/mesh.05_hillslope_noduff.smtk demo-05-spinup-gi/
cp ${TESTS}/test_demos/hillslope_noduff.exo demo-05-spinup-gi/
pvpython $BUILDER \
  $TEMPLATE \
  "${TESTS}/test_demos/demo.05_spinup_gi.yml" \
  -m "demo-05-spinup-gi/mesh.05_hillslope_noduff.smtk" \
  -o demo-05-spinup-gi/demo.05_spinup_gi.smtk
pvpython $EXPORTER demo-05-spinup-gi/demo.05_spinup_gi.smtk \
  -o demo-05-spinup-gi/demo.05_spinup_gi.xml


# name="rock_creek-spinup-homo"
# wkdir="demo-rock_creek-spinup-homo"
# mkdir -p $wkdir
# cp ${TESTS}/test_rock_creek/data/* $wkdir/
# pvpython $BUILDER \
#   $TEMPLATE \
#   "${TESTS}/test_rock_creek/spinup-homo.yml" \
#   -m $wkdir/mesh.rock_creek.smtk \
#   -o $wkdir/demo.${name}.smtk
# pvpython $EXPORTER $wkdir/demo.${name}.smtk \
#   -o $wkdir/demo.${name}.xml
