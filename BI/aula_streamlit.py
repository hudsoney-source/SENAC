import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("salarios1.csv" , encoding='utf-8', sep=';'    )
print(df.head())
print('='*70)

df = df.replace('-', '0')
print(df.head(10))

df.dtypes

tipos = df['2014'].apply(type)
print(tipos)

df.iloc[:, 1:] = df.iloc[:, 1:].apply(lambda col: pd.to_numeric(col.strreplace('.', '', regex-False).str.replace(',', ',', regex=False), errors='coerce'))
print(df.head(10))


