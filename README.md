# Fundamental Limits From Chaos On Instability Time Predictions In Compact Planetary Systems

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3461173.svg)](https://doi.org/10.5281/zenodo.3461173)

This repository contains the source code to reproduce the simulations and figures from Hussain & Tamayo (2019). The figure notebooks can be run directly from the csv files in the repo.

To access the binary files directly, we have uploaded all the data to https://zenodo.org/record/3461173 (10.4 GB). You should untar that file at the root level of the repository, which will create a hussain2019data folder where the Analysis and csvs folders are. The various scripts require several pip installable python libraries (jupyter, matplotlib, numpy, pandas, scipy). You will also have to clone specifically this REBOUND fork: https://github.com/dtamayo/rebound.git

The integrations were run with two different versions of REBOUND, so there are two python scripts that need to be run to generate the CSV files. In your REBOUND directory git checkout 07d10d1e0d96d9e945ae97a78db9b2028c3ef069, then go back to StabilitySetImage and python generate\_old\_csvs.py. Then in your REBOUND directory git checkout 6fb912f615ca542b670ab591375191d1ed914672, go back to StabilitySetImage and python generate\_new\_csvs.py. This will regenerate all the CSVs needed to run the figure scripts. Note that the csvs under csvs/external do not come from this dataset, so those are not regenerated.
