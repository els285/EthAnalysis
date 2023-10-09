!/bin/bash

if ! [[ $# -eq 1 ]] ; then
    echo "Usage: source ${0} <architecture>"
    echo "Where <architecture> is the architecture specification used by lsetup from cvmfs"
    echo "Example architecture: x86_64-centos7-gcc8-opt"
    return 1
fi

# store setup gcc + linux version for future setup and for setup on grid
echo ${1} > atlas_env/architecture.txt
export LCG_ARCH=${1}
# store absolute path to fbuenv (with traversed symlinks) for migating
# to migrate fbuenv we need to know the old absolute paths to overwrite in new location
# this is needed for running on grid, where we send the virtualenv in a tarball
echo `readlink -f $PWD` >> atlas_env/architecture.txt

shopt -s expand_aliases
if [[ -z ${ATLAS_LOCAL_ROOT_BASE+x} ]] ; then
  export ATLAS_LOCAL_ROOT_BASE='/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase'
fi
alias setupATLAS="source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh"

# Set up ATLAS ROOT-python3-virtualenv compatible environment
echo "> setupATLAS"
setupATLAS --quiet
echo "> Setup Python3+ROOT"
lsetup "views LCG_101 x86_64-centos7-gcc8-opt" --quiet
