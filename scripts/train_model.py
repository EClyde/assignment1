"""Real sensor CSV -> train DBSCAN -> KDE uint8 lookup -> model header.
Edryn Clyde Fernandez. Run from repository root.
"""
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN
from sklearn.neighbors import KernelDensity
from sklearn.model_selection import train_test_split

N, TAU, SEED = 16, 0.12, 20261016

def predict(x, tables):
    ij = np.clip(np.floor(x * N).astype(int), 0, N-1)
    votes = tables[:, ij[:, 1], ij[:, 0]].T
    winner = np.argmax(votes, axis=1)
    return np.where(votes[np.arange(len(winner)), winner] >= round(TAU*255), winner, -1)

def main():
    out = Path("outputs")
    out.mkdir(exist_ok=True)
    df = pd.read_csv("data/raw/data_complete.csv")
    if not {"uv_sensor", "IR_sensor", "label"}.issubset(df.columns):
        raise ValueError("Required: uv_sensor,IR_sensor,label")
    counts = df.label.value_counts()
    if len(counts) not in (3, 4) or counts.min() < 500:
        raise ValueError("Need at least 500 real readings for each of 3-4 classes")
    x = np.log1p(df[["uv_sensor", "IR_sensor"]].to_numpy(float))
    y = df.label.astype(str).to_numpy()
    train, other = train_test_split(np.arange(len(y)), test_size=.4, random_state=SEED, stratify=y)
    valid, test = train_test_split(other, test_size=.5, random_state=SEED, stratify=y[other])
    lower, upper = x[train].min(axis=0), x[train].max(axis=0)
    if np.any(upper <= lower):
        raise ValueError("A sensor is constant")
    scaled = (x-lower)/(upper-lower)
    cluster = DBSCAN(eps=.018, min_samples=8).fit_predict(scaled[train])
    ids = sorted(set(cluster)-{-1})
    if not ids: raise ValueError("No clusters: adjust DBSCAN parameters")
    pd.crosstab(pd.Series(y[train], name="ground_truth"),
                pd.Series(cluster, name="dbscan_cluster")).to_csv(out/"dbscan_vs_ground_truth.csv")
    names = [pd.Series(y[train][cluster == k]).value_counts().index[0] for k in ids]
    centres = (np.arange(N)+.5)/N
    xx, yy = np.meshgrid(centres, centres)
    grid = np.c_[xx.ravel(), yy.ravel()]
    candidates=[]
    for bw in (.015, .025, .04, .06, .09):
        maps=[]
        for k in ids:
            kde=KernelDensity(kernel="gaussian", bandwidth=bw).fit(scaled[train][cluster==k])
            z=np.exp(kde.score_samples(grid)).reshape(N,N)
            maps.append(z/z.max())
        tables=np.rint(np.stack(maps)*255).astype(np.uint8)
        pv=predict(scaled[valid], tables)
        predicted=np.array([names[i] if i>=0 else "UNKNOWN" for i in pv])
        candidates.append(((predicted==y[valid]).mean(),bw,tables))
    score,bw,tables=max(candidates,key=lambda a:(a[0],-a[1]))
    predictions=predict(scaled[test],tables)
    names_pred=[names[i] if i>=0 else "UNKNOWN" for i in predictions]
    pd.crosstab(pd.Series(y[test],name="true_label"),
                pd.Series(names_pred,name="lookup")).to_csv(out/"heldout_confusion.csv")
    bounds=np.array([lower[0],upper[0],lower[1],upper[1]],dtype=np.float32)
    np.savez_compressed(out/"surfaces.npz", tables=tables, bounds=bounds,
                        class_names=np.array(names), bandwidth=bw, grid_n=N, reject_tau=TAU)
    print("Clusters:",len(ids),"; DBSCAN noise:",sum(cluster==-1))
    print("Class names:",names)
    print("Validation:",round(float(score),4),"bandwidth",bw)
    print("Held-out test accuracy:",round(float(np.mean(np.array(names_pred)==y[test])),4))
    print("Table bytes:",tables.size,"plus 16 bytes scaling bounds")
if __name__=="__main__": main()
