#!/usr/bin/env bash

action() {
    local base="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

    export LAW_HOME="$base/.law"
    export LAW_CONFIG_FILE="$base/law.cfg"
    export LUIGI_CONFIG_PATH="$base/luigi.cfg"

    #source /storage/9/mcorrea/local/src/fnlosrc_source.sh

    #export PATH="/storage/9/mcorrea/local/src/NNLOJET_rev4708/driver/bin:$PATH"

    #export PATH="/cvmfs/cms.cern.ch/slc6_amd64_gcc481/external/python/2.7.6/bin:$PWD/law/bin:$PWD/luigi/bin:$PATH"
    #export LD_LIBRARY_PATH="/cvmfs/cms.cern.ch/slc6_amd64_gcc481/external/python/2.7.6/lib:/cvmfs/cms.cern.ch/slc6_amd64_gcc481/external/openssl/0.9.8e__1.0.1/lib:$LD_LIBRARY_PATH"

    export PATH="$base/law/bin:$base/luigi/bin:$PATH"

    export PYTHONPATH="$base/law:$base/luigi:$base/six:$base:$PYTHONPATH"

    export ANALYSIS_PATH="$base"
    export ANALYSIS_DATA_PATH="$ANALYSIS_PATH/data"

    export PATH="/storage/9/mcorrea/local/src/fastNLO/tools:/storage/9/mcorrea/local/src/fastNLO/tools/plotting:$PATH"

    source /cvmfs/grid.cern.ch/emi3ui-latest/etc/profile.d/setup-ui-example.sh

    source /cvmfs/etp.kit.edu/fnlo/fnlosrc_source.sh

    export PATH="/cvmfs/etp.kit.edu/fnlo/src/NNLOJET_rev4708/driver/bin:$PATH"

    source "$( law completion )"
}
action
