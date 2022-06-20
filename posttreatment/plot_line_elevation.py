import pickle
import plotly.graph_objects as go
import plotly.offline

def plot_data(data):
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

    plotly.offline.plot(fig, filename="elevation.html")

if __name__ == "__main__":
    with open('./data.pkl', 'rb') as f:
        data = pickle.load(f)

    plot_data(data)
