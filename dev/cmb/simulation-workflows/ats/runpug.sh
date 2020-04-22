#!/usr/bin/env bash

# Script to generate .sbt files from pug templates
# For convenience only, but in order to use:
#   * pug-cli must be installed
#   * python bindings for libxml must be installed (pip install libxml)

# Get script directory, per http://stackoverflow.com/questions/59895
SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  TARGET="$(readlink "$SOURCE")"
  if [[ $TARGET == /* ]]; then
    SOURCE="$TARGET"
  else
    DIR="$( dirname "$SOURCE" )"
    SOURCE="$DIR/$TARGET" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
  fi
done
RDIR="$( dirname "$SOURCE" )"
DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
echo "script DIR is '$DIR'"

# Render to current working directory
pugfiles=(${DIR}/pug/*.pug)
for pugfile in "${pugfiles[@]}"; do
  # echo $pugfile
  filename="${pugfile##*/}"
  # echo $filename
  basename="${filename%.*}"
  # echo $basename
  rm -f ${basename}.sbt
  pug ${pugfile} --pretty --extension sbt -o ${DIR}
  # python fixmultilinetext.py ${subfolder}/${name}.sbt
done
