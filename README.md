# nnlo-law-analysis

## Project setup

clone respository with submodules:
```
git clone --recursive https://github.com/miguel-sc/nnlo-law-analysis.git
```
open luigi.cfg and edit wlcg_path variable

set environment variables:
```
source setup.sh
```
initialize law for cli auto completion:
```
law db --verbose
```

## Interpolation grid creation

Recommended to run the grid production up to Combine task in single threaded mode:
```
law run Combine
```
Run the rest multithreaded:
```
law run AllPlots --workers 10
```
