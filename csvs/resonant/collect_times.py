import pandas as pd
import numpy as np
import os
import rebound
import sys
#import matplotlib 
#from matplotlib import pyplot as plt
#from scipy.stats import norm
#import matplotlib.mlab as mlab
import gc
'''
restrucutre progam to call bash script
which will call this n times to generate
all the needed datafiles since this for
some reason runs into the issues of having
too many files open, which is new to the
new version of rebound

'''

def get_times(row):   
    print(fcpath+row["runstring"])
    try:
        #sim = rebound.Simulation.from_file(fcpath+row["runstring"])    
        #print(fcpath + row["runstring"] )
        sim = rebound.SimulationArchive(fcpath + row["runstring"])
        columns = ['t']
        #features = [ sim.t ]
        features = sim[-1].t
        print ('{0:.16f}'.format(sim[-1].t))
   
        del sim # an attempt to clear memory        
 
    except Exception as e:
        print(e)
        columns= ['t']
        features = [ np.nan ]
    return pd.Series(features, index=columns)



path = "/mnt/scratch-lustre/nhussain/data/"
#efacs = [1.95,1.9, 1.85, 1.8, 1.75, 1.7, 1.65, 1.6, 1.55, 1.5]
#efacs = [1.6]
#ids = range(12, 101)
#ids = [sys.argv[0]]
files = ['Res_sys_{0}_1e8'.format(sys.argv[1])]
#files = ["j=11k=2Zstar=0.3libfac=0.0.bin_1e8"]
#files = ["j=5k=2Zstar=0.03libfac=1.5.bin_1e8"]


#print(files)
#        'solar_efac3_1e9', 'solar_efac2.5_1e9',
#        'solar_efac2_1e9'] 

#, 'solar_efac3.5_1e9','solar_efac4_1e9']
#files = ["res4.bin_1e8","res5.bin_1e8", "res6.bin_1e8" ]
#    "res4.bin_1e8","res5.bin_1e8", "res6.bin_1e8" ]
#files = [ "TwoPlanets1.bin_1e8", "TwoPlanets2.bin_1e8", "TwoPlanets3.bin_1e8"]

#'''
for file_name in files:
    #gc.collect()
    fcpath = path + "resonant_distributions/{0}/simulation_archives/sa".format(file_name)
    #print(file_name)
    df= pd.read_csv(path+"/resonant_distributions/{0}/{1}.csv".format(file_name, file_name.split("_")[2].split("_")[0] ))
    df = pd.concat([df, df.apply(get_times, axis = 1)], axis = 1)
    df.to_csv("{0}{1}.csv".format(file_name.split("1e")[0],df.shape[0] ), index = False)
    del df
    #gc.collect()
    #print( "{0}{1}.csv".format(file_name.split("1e")[0],df.shape[0] ))
    #print(df)
    #break
#print(df)
#'''
