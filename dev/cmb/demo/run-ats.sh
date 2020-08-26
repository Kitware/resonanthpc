#! /bin/sh
# Accepts name of directory with simulation input deck
set -e
# Outputs will be saved there as well in `sim_dump`
pushd $1
rm -rf sim_dump
original_files=$(ls | grep -Ev '\.(smtk|ipynb)$')
mkdir sim_dump
for entry in $original_files
do
  cp $entry sim_dump/$entry
done
cd sim_dump

HOST_MNT=$PWD
CONT_MNT=/home/amanzi_usr/work
CONT_PWD=/home/amanzi_usr/work

# WARNING: If there are more than one, this won't work
input_file=($(find . -type f -name "*.xml"))

docker run --rm -v $HOST_MNT:$CONT_MNT:delegated -w $CONT_PWD metsi/ats mpirun -n 4 ats --xml_file=$input_file

# Return
popd
