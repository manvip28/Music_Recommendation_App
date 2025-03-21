import pandas as pd
from sklearn.preprocessing import StandardScaler
from annoy import AnnoyIndex

df = pd.read_csv("tracks_features.csv")

features = ['danceability', 'energy', 'loudness', 'speechiness', 
            'acousticness', 'instrumentalness', 'liveness', 
            'valence', 'tempo', 'duration_ms', 'year']

# Feature Scaling
df = df.dropna(subset=['name'] + features)
X = df[features].values
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Build Annoy Index
annoy_index = AnnoyIndex(len(features), 'euclidean')
for i, row in enumerate(X_scaled):
    annoy_index.add_item(i, row)
annoy_index.build(10)
