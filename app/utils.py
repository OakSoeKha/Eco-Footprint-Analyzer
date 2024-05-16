import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import random

months = ["January", "Febuary", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"]


def ElectricityBill(kWh, multiple_series=False) -> None:
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
        "app/static/graphs/electricity-bill.html")


def WaterBill(cubic_m, multiple_series=False) -> None:
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

    fig.write_html("app/static/graphs/water-bill.html")


def RevenueToCF(revenue: np.array, CF: np.array, names: np.array) -> None:
    fig = px.scatter(x=CF, y=revenue, labels={
                     "x": "Carbon Emissions", "y": "Revenue"}, hover_name=names, size=revenue)
    fig.update_traces(text=names)
    fig.update_traces(marker=dict(opacity=1))
    fig.update_traces(
        hovertemplate="<b>%{hovertext}</b><br>Carbon Emissions: %{x} billion tonnes<br>Revenue: %{y} billion dollars")
    fig.update_layout(template='plotly_dark')
    fig.write_html("app/static/graphs/revenue-cf.html")


def EmissionsBar(**kwargs) -> None:
    fig = px.bar(x=months, y=kwargs["emission"],
                 labels={"x": "Months", "y": "Emissions"})
    fig.update_traces(hoverinfo='text', hovertext=[f'{name}: {
                      value}' for name, value in zip(months, kwargs["emission"])])
    fig.update_layout(template='plotly_dark')
    fig.write_html("app/static/graphs/emissions.html")


def PercentageChart(**kwargs) -> None:
    labels = list(kwargs.keys())
    values = list(kwargs.values())

    fig = go.Figure(go.Pie(labels=labels, values=values))
    fig.update_traces(hoverinfo='label+percent')
    fig.update_layout(template='plotly_dark')

    fig.write_html(
        "app/static/graphs/percentage-chart.html")
