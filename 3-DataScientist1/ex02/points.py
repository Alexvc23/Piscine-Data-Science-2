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
dataTest = pd.read_csv("../data/Test_knight.csv")

# %%
dataTrain = pd.read_csv("../data/Train_knight.csv")

# %%
PullTest = [dataTest['Pull'][i] for i in range(len(dataTest['Pull']))]
PushTest = [dataTest['Push'][i] for i in range(len(dataTest['Push']))]

# %%
FriendshipTest = [dataTest['Friendship'][i] for i in range(len(dataTest['Friendship']))]
EmpoweredTest = [dataTest['Empowered'][i] for i in range(len(dataTest['Empowered']))]

# %%
GroupTrain = dataTrain.groupby('knight').apply(lambda x : x)

# %%
fig = plt.figure(figsize=(25,25))

plot = plt.subplot2grid((6, 5), (0, 0), fig=fig)

plot.scatter(PullTest, PushTest, label='Knight', color='#7fbf7f')
plot.set_xlabel('Pull')
plot.set_ylabel('Push')
plot.legend()

plot = plt.subplot2grid((6, 5), (0, 1), fig=fig)

plot.scatter(EmpoweredTest, FriendshipTest, label='Knight', color='#7fbf7f')
plot.set_xlabel('Friendship')
plot.set_ylabel('Empowered')
plot.legend()

plot = plt.subplot2grid((6, 5), (1, 1), fig=fig)

plot.scatter(GroupTrain['Empowered']['Sith'], GroupTrain['Friendship']['Sith'], label='Sith', color='red', alpha=0.5)
plot.scatter(GroupTrain['Empowered']['Jedi'], GroupTrain['Friendship']['Jedi'], label='Jedi', color='blue', alpha=0.5)
plot.set_xlabel('Friendship')
plot.set_ylabel('Empowered')
plot.legend()

plot = plt.subplot2grid((6, 5), (1, 0), fig=fig)

plot.scatter(GroupTrain['Pull']['Sith'], GroupTrain['Friendship']['Sith'], label='Sith', color='red', alpha=0.5)
plot.scatter(GroupTrain['Push']['Jedi'], GroupTrain['Friendship']['Jedi'], label='Jedi', color='blue', alpha=0.5)
plot.set_xlabel('Pull')
plot.set_ylabel('Push')
plot.legend()

plt.legend(loc="upper right")
plt.show()