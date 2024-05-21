import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import plotly.graph_objs as go
from colour import Color

months = ["January", "Febuary", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"]


def ElectricityBill(kWh, id, multiple_series=False) -> None:
    fig = go.Figure()
    if not multiple_series:
        fig.add_trace(go.Scatter(x=months, y=kWh,
                      mode='lines+markers', name='Data'))
    else:
        for i, data in enumerate(kWh):
            fig.add_trace(go.Scatter(
                x=months, y=data, mode='lines+markers', name=f'Data {i+1}'))

    fig.update_layout(xaxis=dict(tickmode='array', tickvals=months, ticktext=[str(month) for month in months]),
                      yaxis=dict(title='Kilo-watt hours'),
                      template='plotly_dark')
    fig.write_html(
        f"app/static/graphs/e-{id}.html")


def WaterBill(cubic_m, id, multiple_series=False) -> None:
    fig = go.Figure()
    if not multiple_series:
        fig.add_trace(go.Scatter(x=months, y=cubic_m,
                      mode='lines+markers', name='Data'))
    else:
        for i, data in enumerate(cubic_m):
            fig.add_trace(go.Scatter(
                x=months, y=data, mode='lines+markers', name=f'Data {i+1}'))

    fig.update_layout(xaxis=dict(tickmode='array', tickvals=months, ticktext=[str(month) for month in months]),
                      yaxis=dict(title='Cubic Meters'),
                      template='plotly_dark')

    fig.write_html(f"app/static/graphs/w-{id}.html")


def RevenueToCF(revenue: np.array, CF: np.array, names: np.array, id) -> None:
    revenue_million = revenue * 1e-6  # convert to millions
    CF_billion_tonnes = CF  # already in billion tonnes
    fig = px.scatter(x=CF_billion_tonnes, y=revenue_million, labels={
                     "x": "Carbon Emissions (billion tonnes)", "y": "Revenue (millions)"}, hover_name=names, size=revenue_million)
    fig.update_traces(text=names)
    fig.update_traces(marker=dict(opacity=1))
    fig.update_traces(
        hovertemplate="<b>%{hovertext}</b><br>Carbon Emissions: %{x} billion tonnes<br>Revenue: %{y} million dollars")
    fig.update_layout(template='plotly_dark')
    fig.write_html(f"app/static/graphs/rcf-{id}.html")


def EmissionsBar(**kwargs) -> None:
    fig = px.bar(x=months, y=kwargs["emission"],
                 labels={"x": "Months", "y": "Emissions (billion tonnes)"})
    fig.update_traces(hoverinfo='text', hovertext=[f'{name}: {
                      value}' for name, value in zip(months, kwargs["emission"])])
    fig.update_layout(template='plotly_dark')
    fig.write_html(f"app/static/graphs/e-{kwargs[id]}.html")


def generate_purple_shades(base_color, num_shades):
    base_color = mcolors.to_rgb(base_color)
    return [mcolors.to_hex((base_color[0] * (1 - i / num_shades) + 1 * (i / num_shades),
                            base_color[1] * (1 - i / num_shades) +
                            1 * (i / num_shades),
                            base_color[2] * (1 - i / num_shades) + 1 * (i / num_shades)))
            for i in range(num_shades)]


def PercentageChart(**kwargs) -> None:
    labels = list(kwargs.keys())
    values = list(kwargs.values())

    # Generate different shades of the base color
    num_shades = len(labels)
    base_color = "#636EFA"
    colors = generate_purple_shades(base_color, num_shades)

    fig = go.Figure(go.Pie(labels=labels, values=values,
                    marker=dict(colors=colors)))
    fig.update_traces(hoverinfo='label+percent')
    fig.update_layout(template='plotly_dark')

    fig.write_html(
        f"C:/Users/Lenovo/Documents/Code/projects/Eco-Footprint-Analyzer/app/static/graphs/p-{id}.html")
