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

# %%
dataTrain = pd.read_csv("../data/Train_knight.csv")


# %%
knight = dataTrain.groupby('knight').apply(lambda x : x)

# %%
cor = knight.replace({'knight': 'Jedi'}, 1)
cor = cor.replace({'knight': 'Sith'}, 0)

cor = cor.corr()

cor = cor.sort_values(by='knight',ascending=False)

print(cor['knight'])