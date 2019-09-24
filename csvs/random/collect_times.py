import pandas as pd
import numpy as np
import os
import rebound
import sys
import gc

def get_times(row):
    print(fcpath+row["runstring"])
    try:
        sim = rebound.SimulationArchive(fcpath + row["runstring"])
        columns = ['t']
        features = sim[-1].t
        print ('{0:.16f}'.format(sim[-1].t))

        del sim     

    except Exception as e:
        print(e)
        columns= ['t']
        features = [ np.nan ]
    return pd.Series(features, index=columns)



path = "../data/"
files = ['Sys_{0}_1e8'.format(sys.argv[1])]


for file_name in files:
    fcpath = path + "random_distributions/{0}/simulation_archives/sa".format(file_name)
    df= pd.read_csv(path+"random_distributions/{0}/{1}.csv".format(file_name, file_name.split("_")[1] ))
    df = pd.concat([df, df.apply(get_times, axis = 1)], axis = 1)
    df.to_csv("random_features/{0}1e8.csv".format(file_name.split("1e")[0] ), index = False)
    del df
