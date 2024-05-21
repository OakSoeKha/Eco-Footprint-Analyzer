import numpy as np
import requests
import json

# Constants for emissions rates
EMISSIONS_RATES = {
    "kWh": 0.3900894 / 1e12,  # billion tonnes per kWh
    "cubic_m": 10.5 / 1e12    # billion tonnes per cubic meter
}

# Constants for industry weights
INDUSTRY_WEIGHTS = {
    "Agriculture": None,
    "Technology": 0.06,
    "Finance": None,
    "Healthcare": None,
    "Education": 0.03,
    "Manufacturing": 0.075,
    "Retail": None,
    "Transportation": None,
    "Hospitality": None,
    "Media & Entertainment": 0.04
}

# Function to classify income


def classify_income(gdp_per_capita):
    if not isinstance(gdp_per_capita, (int, float)):
        raise ValueError("GDP per capita must be a number")
    if gdp_per_capita < 500:
        return 0
    elif 500 <= gdp_per_capita <= 2000:
        return (gdp_per_capita - 500) / (2000 - 500)
    elif 2001 <= gdp_per_capita <= 10000:
        return (gdp_per_capita - 2000) / (10000 - 2000)
    elif 10001 <= gdp_per_capita <= 50000:
        return (gdp_per_capita - 10000) / (50000 - 10000)
    elif 50001 <= gdp_per_capita <= 100000:
        return (gdp_per_capita - 50000) / (100000 - 50000)
    else:
        return 1

# Function to fetch GDP for a given country


def get_gdp(country):
    if not isinstance(country, str):
        raise ValueError("Country name must be a string")
    api_url = f"https://api.api-ninjas.com/v1/country?name={country}"
    api_key = "nQ+01VGBAS76VC3ulQPblw==TEbhwrd0Vts2MoQO"
    try:
        response = requests.get(api_url, headers={"X-Api-Key": api_key})
        if response.status_code == requests.codes.ok:
            try:
                return json.loads(response.text)[0]["gdp_per_capita"]
            except (IndexError, KeyError):
                raise ValueError("Country GDP not found")
        else:
            response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        # Fallback value for testing purposes
        return 10000

# Function to calculate carbon footprint


def calculate_carbon_footprint(employee_count, electricity_usage, water_usage, revenue, industry, location):
    # Convert input parameters to numpy arrays
    employee_count = np.array(employee_count)
    electricity_usage = np.array(electricity_usage)
    water_usage = np.array(water_usage)

    annual_water = []
    annual_electricity = []
    annual_employee = []

    # Error checking for input arrays
    if not all(isinstance(arr, np.ndarray) for arr in [employee_count, electricity_usage, water_usage]):
        raise ValueError("All input parameters must be numpy arrays")
    if len(set(len(arr) for arr in [electricity_usage, water_usage])) != 1:
        raise ValueError("Monthly parameters should have the same size")

    # Error checking for industry
    if industry not in INDUSTRY_WEIGHTS:
        raise ValueError("Invalid industry")

    # Error checking for industry weight
    industry_weight = INDUSTRY_WEIGHTS[industry]
    if industry_weight is None:
        raise ValueError(f"Industry weight for {industry} is not defined")

    gdp = classify_income(gdp_per_capita=get_gdp(country=location))
    weight = 0
    if gdp == 1 or gdp == 0:
        weight = 1
    elif gdp <= 0.4285714285714286:
        weight = 0.4 + abs(0.4285714285714286 - gdp) * 1.5
    else:
        weight = 0.8 - abs(0.5714285714285714 - gdp) * 1.5

    # Calculate emissions for each month
    monthly_emissions = []
    for i in range(len(electricity_usage)):
        # Calculate emissions for electricity and water usage for this month
        electricity_emissions = EMISSIONS_RATES["kWh"] * electricity_usage[i]
        water_emissions = EMISSIONS_RATES["cubic_m"] * water_usage[i]

        # Calculate scope 1 emissions
        scope1_emissions = electricity_emissions + water_emissions

        # Calculate scope 2 emissions
        scope2_emissions = employee_count * 4700 * \
            (1 + weight) / 1e12  # converting to billion tonnes

        # Calculate total emissions including revenue-related emissions
        total_emissions = scope1_emissions + scope2_emissions + \
            (revenue * 1e-6 * weight * industry_weight / 12)  # revenue in millions

        # Round each element in the array to 10 decimal places
        rounded_emissions = np.round(total_emissions, 10)

        # Append the rounded emissions to the monthly_emissions list
        monthly_emissions.append(rounded_emissions)

        annual_electricity.append(electricity_emissions)
        annual_water.append(water_emissions)
        annual_employee.append(scope2_emissions)

    return np.array(monthly_emissions), annual_electricity, annual_water, annual_employee


def parse(string) -> list:
    result = string.split(", ")
    return result
