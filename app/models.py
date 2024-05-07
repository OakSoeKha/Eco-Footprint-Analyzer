import random
import numpy as np
import requests
import json


def ClassifyIncome(gdp_per_capita):
    if gdp_per_capita <= 2000:
        return 0
    elif 2001 <= gdp_per_capita <= 10000:
        return (gdp_per_capita - 2000) / (10000 - 2000)
    elif 10001 <= gdp_per_capita <= 40000:
        return (gdp_per_capita - 10000) / (40000 - 10000)
    else:
        return 1


def GetGDP(country):
    api_url = f"https://api.api-ninjas.com/v1/country?name={country}"
    api_key = "nQ+01VGBAS76VC3ulQPblw==TEbhwrd0Vts2MoQO"

    response = requests.get(api_url, headers={"X-Api-Key": api_key})

    if response.status_code == requests.codes.ok:
        return response.text[0]
    else:
        return ("Error:", response.status_code, response.text)


def CFcalculator(employee_count: np.array, electricity_bill: np.array, electricity_price, water_bill: np.arange, water_price, revenue, industry) -> np.array:
    industry_weights = {
        "Tech": 0.06,
        "Manufacturing": 0.075,
        "Entertainment": 0.04,
        "Education": 0.03,
        "Advertising": 0.035,
        "Business Services": 0.05
    }

    emissions = np.array()
    kWh = electricity_bill//electricity_price  # Array of montly kWh used
    cubic_m = water_bill//water_price  # Array of monthly cubic_m of water used

    rates = {  # Emissions in kg per kWh and cubic_m
        "kWh": 0.3900894,
        "cubic_m": 10.5
    }
    resulting_emissions = np.array(size=12)
    for i in range(12):
        scope1 = ((rates["kWh"] * kWh[i]) + (rates["cubic_m"] * cubic_m[i]))
        scope2 = employee_count[i] * 4700
        result = (scope1 + scope2)



