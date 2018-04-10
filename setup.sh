#!/usr/bin/env bash

action() {
    local base="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

    #export PATH="/portal/ekpbms1/home/mcorrea/.local/bin:${PATH}"
    #export LD_LIBRARY_PATH="/portal/ekpbms1/home/mcorrea/.local/lib:${LD_LIBRARY_PATH}"

    #export PYTHONPATH="/portal/ekpbms1/home/mcorrea/src/law:/portal/ekpbms1/home/mcorrea/.local/lib/python3.5/site-packages:/portal/ekpbms1/home/mcorrea/.local/lib/python2.7/site-packages:$base:$PYTHONPATH"
    export LAW_HOME="$base/.law"
    export LAW_CONFIG_FILE="$base/law.cfg"
    export LUIGI_CONFIG_PATH="$base/luigi.cfg"

    export PATH="/cvmfs/cms.cern.ch/slc6_amd64_gcc481/external/python/2.7.6/bin:$PWD/law/bin:$PWD/luigi/bin:$PATH"
    export LD_LIBRARY_PATH="/cvmfs/cms.cern.ch/slc6_amd64_gcc481/external/python/2.7.6/lib:/cvmfs/cms.cern.ch/slc6_amd64_gcc481/external/openssl/0.9.8e__1.0.1/lib:$LD_LIBRARY_PATH"

    export PYTHONPATH="$PWD/law:$PWD/luigi:$PWD/six:$PWD:$PYTHONPATH"

    export ANALYSIS_PATH="$base"
    export ANALYSIS_DATA_PATH="$ANALYSIS_PATH/data"

    source /cvmfs/grid.cern.ch/emi3ui-latest/etc/profile.d/setup-ui-example.sh

    source /cvmfs/etp.kit.edu/fnlo/fnlosrc_source.sh

    export PATH="/cvmfs/etp.kit.edu/fnlo/src/NNLOJET_rev4585/driver/bin:$PATH"

    source "$( law completion )"
}
action
