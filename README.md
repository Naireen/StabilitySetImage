Fundamental Limits From Chaos On Instability Time Predictions In Compact Planetary Systems

This repository contains the source code to reproduce the simulations and figures from Hussain & Tamayo (2019). The figure notebooks can be run directly from the csv files in the repo.

To access the binary files directly, we have uploaded all the data to {insert zenodo link}. That directory should be placed at the root level of the repository, i.e., where the Analysis and csvs folders are. The various scripts require several pip installable python libraries (jupyter, matplotlib, numpy, pandas, scipy). You will also have to clone specifically this REBOUND fork: https://github.com/dtamayo/rebound.git

To begin, we first need to generate the CSV files for visualization from the simulation archive files. To do this, execute generate_data.sh

Once this is done, the csv's file with the instability times will be generated. The next step would be to run the notebooks Analysis/Random_Guassian_Fits.ipynb and Analysis/Resonant_Guassian_Fits.ipynb. After this, you can run any of the notebooks labelled Figure*.ipynb to generate all the figures.
