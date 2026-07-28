import pandas as pd

df = pd.read_csv("data/weatherAUS.csv")

print(df.shape)
print(df.head())
print(df["RainTomorrow"].value_counts())