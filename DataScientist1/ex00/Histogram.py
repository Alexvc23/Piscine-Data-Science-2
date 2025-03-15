
import sqlalchemy
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import matplotlib.ticker as ticker 
from sklearn.cluster import KMeans
from datetime import datetime
from pytz import timezone



data = pd.read_csv("/app/knight/Test_knight.csv")


n_bins = 40
colums = len(data.columns)
row = colums // 5

fig = plt.figure(figsize=(25,25))

for i in range(row):
    for j in range(5):
        plot = plt.subplot2grid((6, 5), (i, j), fig=fig)
        name = data.columns[i * 5 + j]
        plot.hist(data[name], bins=n_bins, color='#7fbf7f', label='Knight')
        plot.set_title(name)
        plot.legend(loc="upper right")

plt.show()



dataTrain = pd.read_csv("/app/knight/Train_knight.csv")

fig = plt.figure(figsize=(25,25))

knight = dataTrain.groupby('knight').apply(lambda x : x)

for i in range(row):
    for j in range(5):
        plot = plt.subplot2grid((6, 5), (i, j), fig=fig)
        name = data.columns[i * 5 + j]
        plot.hist(knight[name]['Sith'], bins=n_bins, color='red', alpha=0.5, label='Sith')
        plot.hist(knight[name]['Jedi'], bins=n_bins, color='blue', alpha=0.5, label='Jedi')
        plot.set_title(name)
        plot.legend(loc="upper right")

plt.show()



cor = knight.replace({'knight': 'Jedi'}, 1)
cor = cor.replace({'knight': 'Sith'}, 0)

cor = cor.corr()

cor = cor.sort_values(by='knight',ascending=False)

print(cor['knight'])