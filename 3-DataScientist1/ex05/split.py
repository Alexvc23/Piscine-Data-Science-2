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

# Split dataset into Training and Validation sets
Training, Validation = train_test_split(dataTrain, test_size=0.25, random_state=42)

print(f"Training dataframe shape: {Training.shape}, with {Training.shape[0]} rows and {Training.shape[1]} columns")
print(Training.head(5))

print(f"\nValidation dataframe shape: {Validation.shape}, with {Validation.shape[0]} rows and {Validation.shape[1]} columns")
print(Validation.head(10))


# %%
Training.to_csv("Training_knight.csv", index=False)
Validation.to_csv("Validation_knight.csv", index=False)
# %%
