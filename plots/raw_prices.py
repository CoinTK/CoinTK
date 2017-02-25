from plotly.offline import plot
import plotly.graph_objs as go
from cointk.data import load_coinbase_usd, subarray_with_stride, to_datetimes


_, data, _ = load_coinbase_usd()
print(data.shape)

plot_data = subarray_with_stride(data, 100)
print(plot_data.shape)
times = to_datetimes(plot_data[:, 0])
scatter = go.Scatter(x=times, y=plot_data[:, 1])
traces = [scatter]
layout = go.Layout(
    title='BTC USD over time',
    yaxis=dict(
        title='USD'
    )
)
plot(go.Figure(data=traces, layout=layout))
