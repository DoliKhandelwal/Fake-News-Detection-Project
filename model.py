import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import glob
import nltk
import re

nltk.download('stopwords')
from nltk.corpus import stopwords

csv_files = ["FakeNewsNet.csv","true.csv","fake.csv","bbc_news.csv","fake_and_real_news.csv"]  
dataframes = []

for file in csv_files:
    df = pd.read_csv(file)
    if 'title' in df.columns and 'text' in df.columns:
        df['content'] = df['title'].astype(str) + " " + df['text'].astype(str)
    elif 'text' in df.columns:
        df['content'] = df['text'].astype(str)
    elif 'headline' in df.columns:
        df['content'] = df['headline'].astype(str)
    if 'label' in df.columns:
        df = df[['content', 'label']]
    elif 'real' in df.columns:
        df.rename(columns={'real': 'label'}, inplace=True)
        df = df[['content', 'label']]
    else:
        continue
    dataframes.append(df)

# Combine all datasets
data = pd.concat(dataframes, ignore_index=True)
