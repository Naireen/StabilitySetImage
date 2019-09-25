import pandas as pd
import numpy as np
import os
import rebound
import sys
import gc

def get_times(row):
    print(fcpath+row["runstring"])
    try:
        sim = int(rebound.SimulationArchive(fcpath + row["runstring"]))
        columns = ['t']
        features = sim[-1].t
        print ('{0:.16f}'.format(sim[-1].t))
        del sim
    except Exception as e:
        print(e)
        columns= ['t']
        features = [ np.nan ]
    return pd.Series(features, index=columns)


def get_times_trappist(row):
    run_number = int(row["runstring"].split(".")[0])
    sim_path = fcpath+str(run_number)+".bin"
    print(sim_path)
    try:
        sim = int(rebound.SimulationArchive(fcpath + sim_path))
        columns = ['t']
        features = sim[-1].t
        print ('{0:.16f}'.format(sim[-1].t))
        del sim
    except Exception as e:
        print(e)
        columns= ['t']
        features = [ np.nan ]
    return pd.Series(features, index=columns)

path = "../data/other_distributions"
files = ['solar_1.4_1e9_200', 'solar_1.45_1e9_200']

for file_name in files:
    fcpath = path + "other_distributions/{0}/simulation_archives/sa".format(file_name)
    df= pd.read_csv(path+"other_distributions/{0}/times.csv".format(file_name))
    df = pd.concat([df, df.apply(get_times, axis = 1)], axis = 1)
    df.to_csv("{0}.csv".format(file_name), index = False)
    del df

files = ['trap_ic4_1e8']
for file_name in files:
    fcpath = path + "other_distributions/{0}/simulation_archives/sarunstring".format(file_name)
    df= pd.read_csv(path+"other_distributions/{0}/times.csv".format(file_name))
    df = pd.concat([df, df.apply(get_times_trappist, axis = 1)], axis = 1)
    df.to_csv("{0}.csv".format(file_name), index = False)
    del df
    break
             
