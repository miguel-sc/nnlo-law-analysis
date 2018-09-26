#!/usr/bin/env bash

action() {

    export PATH="/cvmfs/cms.cern.ch/slc6_amd64_gcc481/external/python/2.7.6/bin:$PATH"
    export LD_LIBRARY_PATH="/cvmfs/cms.cern.ch/slc6_amd64_gcc481/external/python/2.7.6/lib:/cvmfs/cms.cern.ch/slc6_amd64_gcc481/external/openssl/0.9.8e__1.0.1/lib:$LD_LIBRARY_PATH"

    # law + luigi env variables
    local base="{{analysis_path}}"
    export LAW_HOME="$base/.law"
    export LAW_CONFIG_FILE="$base/law.cfg"
    export LUIGI_CONFIG_PATH="$base/luigi.cfg"
    export ANALYSIS_PATH="$base"
    export ANALYSIS_DATA_PATH="$ANALYSIS_PATH/data"

    # luigi + law
    export PATH="$base/law/bin:$base/luigi/bin:$PATH"
    export PYTHONPATH="$base/law:$base/luigi:$base/six:$base:$PYTHONPATH"

    # fastNLO tools + plotting
    export PATH="/storage/9/mcorrea/local/src/fastNLO/tools:/storage/9/mcorrea/local/src/fastNLO/tools/plotting:$PATH"

    # gfal2
    source /cvmfs/grid.cern.ch/emi3ui-latest/etc/profile.d/setup-ui-example.sh

    # NNLOJET + APPLfast
    source /cvmfs/etp.kit.edu/nnlo-multicore/fnlosrc_source.sh

    # NNLOJET combine script
    export PATH="/cvmfs/etp.kit.edu/nnlo-multicore/src/NNLOJET_rev5088/driver/bin:$PATH"

}
action
