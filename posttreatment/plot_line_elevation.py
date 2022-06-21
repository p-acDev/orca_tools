import pickle
import plotly.graph_objects as go
import plotly.offline
import sys
from extract_line_elevation import extract_line_elevation
import OrcFxAPI


def plot_data(data, output_filename):
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
        fig.add_trace(go.Scatter3d(x=data[k]['X'], y=data[k]['Y'], z=data[k]['Z'],
                                   name=k,
                                   marker=dict(size=5, color=color)
                                   )
                      )

    plotly.offline.plot(fig, filename=output_filename)

    return None

if __name__ == "__main__":

    data = extract_line_elevation(OrcFxAPI.Model(sys.argv[1]))
    output_filename = f'{sys.argv[1][:-4]}_elevation3D.html'
    plot_data(data)
