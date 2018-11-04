import matplotlib
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np

data = pd.read_csv("Res_sys_0_500.csv", index_col = 0)
plt.hist(data["t"])
plt.show()



