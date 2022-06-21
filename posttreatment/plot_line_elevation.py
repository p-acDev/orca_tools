import pickle
import plotly.graph_objects as go
import plotly.offline
import plotly.express as px
import sys
from extract_line_elevation import extract_line_elevation
import OrcFxAPI
import matplotlib.pyplot as plt
from itertools import product
import pandas as pd

def plot_data(data, input_filename):
    fig = go.Figure()
    for k, v in data.items():
        if 'FRONT' in k:
            color='red'
        elif 'BACK' in k:
            color='blue'
        elif 'LEFT' in k:
            color='green'
        elif 'RIGHT' in k:
            color='orange'
        else:
            color='black'
        fig.add_trace(go.Scatter3d(x=data[k]['X'], y=data[k]['Y'], z=data[k]['Z'],
                                   name=k,
                                   marker=dict(size=5, color=color)
                                   )
                      )

    plotly.offline.plot(fig, filename=f'{input_filename}_elevation3D.html')

    return None

def do_heatmap(input_filename):
    for side1, side2 in product(['FRONT', 'BACK'], ['LEFT', 'RIGHT']):
        try:
            df = pd.read_excel(f'{input_filename}_{side1}_Vs_{side2}_delta_z.xlsx', index_col=0)
            fig = px.imshow(df)
            plotly.offline.plot(fig, filename=f'{input_filename}_{side1}_Vs_{side2}_heatmap_elevation.html')            
            #plt.savefig(f'{input_filename}_{side1}_Vs_{side2}_heatmap_elevation.png')
        except FileNotFoundError:
            print("Heatmap not created as clashing report not done for the moment")
    return None

if __name__ == "__main__":

    data = extract_line_elevation(OrcFxAPI.Model(sys.argv[1]))
    input_filename = sys.argv[1][:-4]

    plot_data(data, input_filename)
    do_heatmap(input_filename)
