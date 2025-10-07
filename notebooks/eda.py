#%%
import pandas as pd
from utils import eda

df_petz = pd.read_csv("../data/bronze/petz_bronze.csv", sep=";", encoding="utf-8")
df_cobasi = pd.read_csv("../data/bronze/cobasi_bronze.csv", sep=";", encoding="utf-8")
df_pop_pet = pd.read_csv("../data/bronze/pop_pet_bronze.csv", sep=";", encoding="utf-8")
df_petland = pd.read_csv("../data/bronze/petland_bronze.csv", sep=";", encoding="utf-8")

df_lojas = pd.read_csv("../data/bronze/lojas_bronze.csv", sep=";", encoding="utf-8")

eda(df_lojas)