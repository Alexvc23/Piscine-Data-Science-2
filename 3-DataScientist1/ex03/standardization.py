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
from sklearn.preprocessing import StandardScaler

# %%
dataTest = pd.read_csv("../data/Test_knight.csv")

# %%
dataTrain = pd.read_csv("../data/Train_knight.csv")

# %%
object= StandardScaler()

fig = plt.figure(figsize=(25,25))

scaleTest = object.fit_transform(dataTest)
scaleTest = pd.DataFrame(scaleTest, columns=dataTest.columns)

data = dataTrain[dataTrain.columns[:-1]]
knightTrain = dataTrain['knight']

data = object.fit_transform(data)
dataTrain = pd.DataFrame(data, columns=dataTrain.columns[:-1])
dataTrain = dataTrain.join(knightTrain)

dataTrain = dataTrain.groupby('knight')

plot = plt.subplot2grid((6, 5), (0, 0), fig=fig)

plot.scatter(dataTrain.get_group('Sith')['Empowered'], dataTrain.get_group('Sith')['Friendship'], label='Sith', color='red', alpha=0.5)
plot.scatter(dataTrain.get_group('Jedi')['Empowered'], dataTrain.get_group('Jedi')['Friendship'], label='Jedi', color='blue', alpha=0.5)
plot.set_xlabel('Empowered')
plot.set_ylabel('Friendship')
plot.legend()

plot = plt.subplot2grid((6, 5), (0, 1), fig=fig)

plot.scatter(scaleTest['Empowered'], scaleTest['Friendship'], label='knight', color='#7fbf7f')
plot.set_xlabel('Empowered')
plot.set_ylabel('Friendship')
plot.legend()