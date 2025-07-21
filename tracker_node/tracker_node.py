from sqlalchemy import create_engine
try:
    from cuml.cluster import DBSCAN
    import cupy as cp
    GPU_AVAILABLE = True
except ImportError:
    from sklearn.cluster import DBSCAN
    import numpy as cp  # alias numpy as cp for compatibility
    GPU_AVAILABLE = False

import pandas as pd
from shared.config import DB_URL

engine = create_engine(DB_URL)

def fetch_data():
    with engine.connect() as conn:
        return pd.read_sql("SELECT * FROM detected_objects", conn)

def deduplicate():
    df = fetch_data()
    if df.empty:
        return []
    X = cp.asarray(df[['x', 'y', 'depth']].values)
    model = DBSCAN(eps=30.0, min_samples=1)
    labels = model.fit_predict(X)
    clusters = {}
    if GPU_AVAILABLE:
        labels = labels.get()
    for idx, label in enumerate(labels):
        clusters.setdefault(label, []).append(df.iloc[idx])
    return [pd.DataFrame(c).mean(numeric_only=True).to_dict() for c in clusters.values()]
