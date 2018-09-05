#!/usr/bin/env bash

action() {

    # law + luigi env variables
    local base="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
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
    source /cvmfs/etp.kit.edu/fnlo/fnlosrc_source.sh

    # NNLOJET combine script
    export PATH="/cvmfs/etp.kit.edu/fnlo/src/NNLOJET_rev4708/driver/bin:$PATH"

    source "$( law completion )"
}
action
