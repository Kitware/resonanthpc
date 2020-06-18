#! bin/sh
# Accepts name of directory with simulation input deck
set -e
# Outputs will be saved there as well in `sim_dump`
pushd $1
rm -rf sim_dump
original_files=($(ls))
echo "Original files: $original_files"

HOST_MNT=$PWD
CONT_MNT=/home/amanzi_usr/work
CONT_PWD=/home/amanzi_usr/work

# WARNING: If there are more than one, this won't work
input_file=($(find . -type f -name "*.xml"))

docker run --rm -v $HOST_MNT:$CONT_MNT:delegated -w $CONT_PWD metsi/ats mpirun -n 4 ats --xml_file=$input_file

mkdir sim_dump
# Migrate the results into a new subdirectory
for entry in $(ls)
do
  if [[ ! "$entry" =~ $original_files && ! "$entry" =~ "sim_dump" ]]; then
    echo "moving $entry"
    mv $entry sim_dump/$entry
  fi
done

# Return
popd
