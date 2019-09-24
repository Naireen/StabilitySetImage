Fundamental Limits From Chaos On Instability Time Predictions In Compact Planetary Systems

This repository contains the source code to reproduce the simulations and figures from Tamayo et al. (2017). The data generation and processing is segmented. We start from data generation to plotting figures.

The various scripts require REBOUND (https://github.com/hannorein/rebound), and fairly standard python libraries (jupyter, matplotlib, numpy, pandas), as well a few more for statistical analysis, such as emcee and scipy.


To begin, we first need to generate the CSV files for visualization from the simulation archive files. To run them, you first have to get the datafiles at {insert zenodo link} and place all the files in the empty data/ directory under csvs. Place the respective distributions in their corresponding directories under data/. Then from the root directory of this Github repository, execute generate_data.sh

Once this is done, the csv's file with the instability times will be generated. The next step would be to run the notebooks Analysis/Random_Guassian_Fits.ipynb and Analysis/Resonant_Guassian_Fits.ipynb. After this, you can run any of the notebooks labelled Figure*.ipynb to generate all the figures.
