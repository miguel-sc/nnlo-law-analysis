#!/usr/bin/env bash

# Bootstrap file for batch jobs that is sent with all jobs and
# automatically called by the law remote job wrapper script to find the
# setup.sh file of this example which sets up software and some environment
# variables. The "{{analysis_path}}" variable is defined in the workflow
# base tasks in analysis/framework.py.

action() {

    export PATH="/cvmfs/cms.cern.ch/slc6_amd64_gcc481/external/python/2.7.6/bin:$PWD/law/bin:$PWD/luigi/bin:$PATH"
    export LD_LIBRARY_PATH="/cvmfs/cms.cern.ch/slc6_amd64_gcc481/external/python/2.7.6/lib:/cvmfs/cms.cern.ch/slc6_amd64_gcc481/external/openssl/0.9.8e__1.0.1/lib:$LD_LIBRARY_PATH"

    source /cvmfs/grid.cern.ch/emi3ui-latest/etc/profile.d/setup-ui-example.sh

    source /cvmfs/etp.kit.edu/fnlo/fnlosrc_source.sh

    export PYTHONPATH="$PWD/law:$PWD/luigi:$PWD/six:$PWD:$PYTHONPATH"

    tar -xzf analysis*.tar.gz
    rm analysis*.tar.gz

    export LAW_HOME="$PWD/.law"
    export LAW_CONFIG_FILE="$PWD/law.cfg"
    export LUIGI_CONFIG_PATH="$PWD/luigi.cfg"

    export ANALYSIS_PATH="$PWD"
    export ANALYSIS_DATA_PATH="$ANALYSIS_PATH"
    law db --verbose

}
action
