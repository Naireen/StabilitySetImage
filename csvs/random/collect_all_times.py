import numpy as np
import os
import pandas as pd
from subprocess import call
#dirs = os.listdir()
#print(len(dirs))
d = '../data/random_distributions'
dirs = [os.path.join(d, o) for o in os.listdir(d) if os.path.isdir(os.path.join(d,o))]
print(len(dirs))

for dir_name in dirs:
    #print(dir_name)
    dir_num = dir_name.split("_")[2]
    call(['python', 'collect_times.py', dir_num])
    break

