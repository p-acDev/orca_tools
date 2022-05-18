import pandas as pd
import numpy as np
from scipy.interpolate import griddata
import pandas as pd
import sys

raw_filename = sys.argv[1]

dx = int(sys.argv[2])
dy = int(sys.argv[3])

df_raw = pd.read_csv(raw_filename, sep=";")

x = df_raw['X']
y = df_raw['Y']
z = df_raw['Z']

xi = np.arange(x.min(), x.max(), dx)
yi = np.arange(y.min(), y.max(), dy)

X, Y = np.meshgrid(xi, yi)

print("\n[*] Building new mesh. please wait ...")

Z = griddata((x, y), z, (X, Y), method='linear')

df_new = pd.DataFrame({"x": X.flatten(), "y": Y.flatten(), "z": Z.flatten()}).dropna()
df_new.to_csv("new_mesh.csv", sep=";")

print("\n[+] New mesh generated")