# %%
import sqlalchemy
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import matplotlib.ticker as ticker 
from sklearn.cluster import KMeans
from datetime import datetime
from pytz import timezone
from sklearn.preprocessing import normalize
from sklearn.preprocessing import StandardScaler

# %%
dataTest = pd.read_csv("../data/Test_knight.csv")

# %%
dataTrain = pd.read_csv("../data/Train_knight.csv")

# %%
def NormalizeMax(array):
    return (array - min(array)) / (max(array - min(array)))

# %%
for i in dataTest:
    dataTest[i] = NormalizeMax(dataTest[i])

# %%
data = dataTrain[dataTrain.columns[:-1]]
knight = dataTrain[dataTrain.columns[-1]]

for i in data:
    data[i] = NormalizeMax(data[i])

data = pd.DataFrame(data, columns=dataTrain.columns[:-1])
data = data.join(knight)


# %%
fig = plt.figure(figsize=(25,25))

plot = plt.subplot2grid((6, 5), (0, 0), fig=fig)

plot.scatter(dataTest["Pull"], dataTest["Push"], label='Knight', color='#7fbf7f')
plot.set_xlabel('Pull')
plot.set_ylabel('Push')
plot.legend()

plot = plt.subplot2grid((6, 5), (0, 1), fig=fig)

plot.scatter(data[data['knight'] == 'Jedi']["Pull"], data[data['knight'] == 'Jedi']["Push"], label='Jedi', color='blue', alpha=0.5)
plot.scatter(data[data['knight'] == 'Sith']["Pull"], data[data['knight'] == 'Sith']["Push"], label='Sith', color='red', alpha=0.5)
plot.set_xlabel('Pull')
plot.set_ylabel('Push')
plot.legend()

plt.show()