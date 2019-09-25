import numpy as np
import emcee
import pandas as pd
import rebound
import os
from scipy.stats import norm, ks_2samp
import dask.dataframe as dd

if rebound.__githash__ != '07d10d1e0d96d9e945ae97a78db9b2028c3ef069':
    print('Check out rebound commit 07d10d1e0d96d9e945ae97a78db9b2028c3ef069 and rerun script')
    exit()

seed = 0
np.random.seed(seed)
nwalkers = 20
ndim = 2
iterations = 1000

def lnprob(p, vec):
    diff = vec-p[0]
    N = len(vec)

    if p[1] <=0:
        return -np.inf
    try:
        probs = -0.5 * N * np.log(2. * np.pi) - N/2. * np.log(np.abs(p[1])**2) - 0.5 \
                                    * np.sum(( (vec - p[0]) / p[1] ) ** 2)
    except:
        probs = 0.00
    return probs
       
def log_prob_normed(mu, sigma, info):
    prob = -np.log(2*np.pi)/2. - np.log(sigma**2.)/2.-(1./(sigma**2.)/2./info.shape[0])*np.nansum((info-mu)**2.)
    return prob

def collision(reb_sim, col):
    reb_sim.contents._status = 5
    return 0

def run(row):
    tmax = 1e7
    ID = int(row['ID'])
    
    systemdir = distpath+'Sys_{0}_1e8/'.format(ID)
    for file in os.listdir(systemdir):
        if 'csv' in file:
            data = pd.read_csv(systemdir+file, index_col=0)
            data = data.apply(get_times, args=(systemdir,), axis=1)
            data.to_csv(csvpath+'Sys_{0}_{1}.csv'.format(ID, data.shape[0]))
            
    realization = data.loc[0]
    row['instability_time'] = realization['t']
    file = distpath+"Sys_{0}_1e8/initial_conditions/ic".format(ID)+realization['runstring']
    
    data = data[data["t"]<1e8]
    data = np.log10(data["t"].values)
    
    p0 = [np.random.rand(ndim) for i in range(nwalkers)]
    sampler = emcee.EnsembleSampler(nwalkers, ndim, lnprob, args=[data], a=5)
    
    # Run 200 steps as a burn-in.
    pos, prob, state = sampler.run_mcmc(p0, 200)
    sampler.reset()
    pos, prob, state = sampler.run_mcmc(pos, iterations, rstate0=seed)
    
    maxprob_indice = np.argmax(prob)
    mean_fit, sigma_fit = pos[maxprob_indice]
    sigma_fit = np.abs(sigma_fit) 
    row['Mean'] = mean_fit
    row['Sigma'] = sigma_fit
    
    test = np.random.normal(loc=row['Mean'], scale=row['Sigma'], size = data.shape[0])

    try:
        statistic, KSpval = ks_2samp(data, test)
    except:
        statistic, KSpval = 0,0
        
    row['KSpval'] = KSpval
    
    sim = rebound.Simulation.from_file(file)
    sim.ri_whfast.keep_unsynchronized = 1
    sim.collision_resolve=collision
    sim.init_megno(seed=0)

    Nout = 1000
    times = np.logspace(0, np.log10(tmax), Nout)
    P0 = sim.particles[1].P

    row['tlyap10'] = np.nan
    row['Nlyap10'] = np.nan
    
    sim.integrate(row['instability_time']/10, exact_finish_time=0)
    row['tlyap10'] = 1/sim.calculate_lyapunov()/P0
    if row['tlyap10'] < 0 or row['tlyap10'] > sim.t:
        row['tlyap10'] = sim.t
    row['Nlyap10'] = row['instability_time']  / row['tlyap10']
    
    return row

def get_times(row, args):
    systemdir = args
    fcpath = systemdir+"/final_conditions/fc"
    try:
        sim = rebound.Simulation.from_file(fcpath + row["runstring"])
        row['t'] = sim.t
        del sim 
    except Exception as e:
        print(e, fcpath)
        row['t'] = np.nan
    return row

# solar system runs

ssdistpath = 'hussain2019data/solarsystem/solar_efac1.45_1e9/'
f = 'times_1.45.csv'
data = pd.read_csv(ssdistpath+f, index_col=0)
data = data.apply(get_times, args=(ssdistpath,), axis=1)

sim = rebound.Simulation.from_file(ssdistpath+'initial_conditions/ic'+data.loc[0, 'runstring'])
P0 = sim.particles[1].P
data['t'] /= P0 # Divide by innermost orbital period (essentially same for all shadows)

data.to_csv('csvs/solar_1.45_1e9_200.csv')

ssdistpath = 'hussain2019data/solarsystem/solar_efac1.4_1e9/'
f = 'times_1.4.csv'
data = pd.read_csv(ssdistpath+f, index_col=0)
data = data.apply(get_times, args=(ssdistpath,), axis=1)

sim = rebound.Simulation.from_file(ssdistpath+'initial_conditions/ic'+data.loc[0, 'runstring'])
P0 = sim.particles[1].P
data['t'] /= P0 # Divide by innermost orbital period (essentially same for all shadows)

data.to_csv('csvs/solar_1.4_1e9_200.csv')

# random systems

csvpath = "csvs/random_distributions/"
distpath = 'hussain2019data/distributions/'
for root, dirs, files in os.walk(distpath):
    planet_systems = dirs
    break

df = pd.DataFrame([s.split("_")[-2] for s in planet_systems], columns=["ID"])
df = df.sort_values("ID")
df = df.reset_index(drop=True)

ddf = dd.from_pandas(df, npartitions=24)
testres = run(df.iloc[0])
df = ddf.apply(run, axis=1, meta=pd.DataFrame([testres])).compute(scheduler='processes')

df.to_csv('csvs/random_summary.csv')
