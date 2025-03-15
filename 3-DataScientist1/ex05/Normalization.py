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
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# %%
dataTrain = pd.read_csv("../data/Train_knight.csv")

# %%
Training, Validation = train_test_split(dataTrain, train_size=0.25, random_state=42)

print(Training)
print(Validation)

# %%
Training.to_csv("Training_knight.csv", index=False)
Validation.to_csv("Validation_knight.csv", index=False)