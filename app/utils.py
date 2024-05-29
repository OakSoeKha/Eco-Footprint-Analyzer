import os
import matplotlib.colors as mcolors
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from flask import url_for

months = ["January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"]

# Define the base directory for the graphs
BASE_DIR = os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'static', 'graphs'))


def ElectricityBill(kWh, ide, multiple_series=False) -> None:
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
    fig.update_layout(title=dict(
        text="Monthly Electric Bills", font=dict(size=30)))

    file_path = os.path.join(BASE_DIR, f"e-{ide}.html")
    fig.write_html(file_path)


def WaterBill(cubic_m, ide, multiple_series=False) -> None:
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
    fig.update_layout(title=dict(
        text="Monthly Water Bills", font=dict(size=30)))

    file_path = os.path.join(BASE_DIR, f"w-{ide}.html")
    fig.write_html(file_path)


def EmissionsBar(**kwargs) -> None:
    ide = kwargs.pop('ide')  # Extract ide from kwargs
    fig = px.bar(x=months, y=kwargs["emission"],
                 labels={"x": "Months", "y": "Emissions (billion tonnes)"})
    fig.update_traces(hoverinfo='text', hovertext=[f'{name}: {
                      value}' for name, value in zip(months, kwargs["emission"])])
    fig.update_layout(template='plotly_dark')
    fig.update_layout(title=dict(
        text="Monthly Emissions", font=dict(size=30)))

    file_path = os.path.join(BASE_DIR, f"em-{ide}.html")
    fig.write_html(file_path)


def generate_purple_shades(base_color, num_shades):
    base_color = mcolors.to_rgb(base_color)
    return [mcolors.to_hex((base_color[0] * (1 - i / num_shades) + 1 * (i / num_shades),
                            base_color[1] * (1 - i / num_shades) +
                            1 * (i / num_shades),
                            base_color[2] * (1 - i / num_shades) + 1 * (i / num_shades)))
            for i in range(num_shades)]


def PercentageChart(**kwargs) -> None:
    ide = kwargs.pop('ide')  # Extract ide from kwargs
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
    fig.update_layout(title=dict(
        text="Emission Contributors", font=dict(size=30)))

    file_path = os.path.join(BASE_DIR, f"p-{ide}.html")
    fig.write_html(file_path)
