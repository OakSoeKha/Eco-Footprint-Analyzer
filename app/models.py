import numpy as np
import requests
import json

# Constants for emissions rates
EMISSIONS_RATES = {
    "kWh": 0.3900894 / 1e6,  # kg CO2e per kWh
    "cubic_m": 10.5 / 1e6    # kg CO2e per cubic meter
}

# Constants for industry weights
INDUSTRY_WEIGHTS = {
    "Agriculture": 0.12,
    "Technology": 0.06,
    "Finance": 0.02,
    "Healthcare": 0.04,
    "Education": 0.03,
    "Manufacturing": 0.075,
    "Retail": 0.05,
    "Transportation": 0.1,
    "Hospitality": 0.03,
    "Media & Entertainment": 0.04,
    "Construction": 0.07,
    "Real Estate": 0.05,
    "Telecommunications": 0.03,
    "Legal": 0.02,
    "Government": 0.03,
    "Non-Profit": 0.01,
    "Arts & Culture": 0.015,
    "Sports": 0.02,
    "Insurance": 0.015,
    "Logistics": 0.06,
    "Pharmaceuticals": 0.03,
    "Biotechnology": 0.02,
    "Automotive": 0.08,
    "Aerospace": 0.09,
    "Defense": 0.07,
    "Food & Beverage": 0.06,
    "Chemicals": 0.08,
    "Mining": 0.11,
    "Textiles": 0.05,
    "Fisheries": 0.04,
    "Forestry": 0.05,
    "Marine": 0.06,
    "Waste Management": 0.07,
    "Security": 0.03,
    "Interior Design": 0.02,
    "Fashion": 0.04,
    "Tourism": 0.03,
    "Publishing": 0.025,
    "Marketing": 0.02,
    "Human Resources": 0.015,
    "IT Services": 0.03,
    "Research": 0.025,
    "Architecture": 0.04,
    "Design": 0.025,
    "E-commerce": 0.03,
    "Gaming": 0.02,
    "Health & Wellness": 0.02
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
    employee_count = np.array([employee_count])
    electricity_usage = np.array(electricity_usage, dtype=float)
    water_usage = np.array(water_usage, dtype=float)

    # Error checking for input arrays
    if not all(isinstance(arr, np.ndarray) for arr in [employee_count, electricity_usage, water_usage]):
        raise ValueError("All input parameters must be numpy arrays")
    if len(electricity_usage) != 12 or len(water_usage) != 12:
        raise ValueError(
            "Electricity and water usage must have 12 monthly values")

    # Error checking for industry
    if industry not in INDUSTRY_WEIGHTS:
        raise ValueError("Invalid industry")

    industry_weight = INDUSTRY_WEIGHTS[industry]
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
    annual_water = []
    annual_electricity = []
    annual_employee = []

    monthly_revenue = revenue / 12.0

    for i in range(len(electricity_usage)):
        # Calculate emissions for electricity and water usage for this month
        # kg CO₂e
        electricity_emissions = EMISSIONS_RATES["kWh"] * electricity_usage[i]
        # kg CO₂e
        water_emissions = EMISSIONS_RATES["cubic_m"] * water_usage[i]

        # Calculate scope 1 emissions
        scope1_emissions = electricity_emissions + water_emissions  # kg CO₂e

        # Calculate scope 2 emissions (assuming an average value for employee emissions)
        # kg CO₂e per employee per month (average estimate)
        employee_emissions = 500
        scope2_emissions = employee_count[0] * employee_emissions  # kg CO₂e

        # Calculate scope 3 emissions (using revenue as a proxy for the business activity)
        scope3_emissions = monthly_revenue * \
            industry_weight * weight  # metric tonnes CO₂e

        # Convert kg CO₂e to metric tonnes and sum up all scopes
        total_emissions = (scope1_emissions / 1e3) + (scope2_emissions /
                                                      1e3) + scope3_emissions  # metric tonnes CO₂e

        # Round each element in the array to 10 decimal places
        rounded_emissions = np.round(total_emissions, 10)

        # Append the rounded emissions to the monthly_emissions list
        monthly_emissions.append(rounded_emissions)

        annual_electricity.append(electricity_emissions)
        annual_water.append(water_emissions)
        annual_employee.append(scope2_emissions)

        # Debugging print statements
        print(f"Month {i+1}:")
        print(f"  Electricity Emissions (kg CO₂e): {electricity_emissions}")
        print(f"  Water Emissions (kg CO₂e): {water_emissions}")
        print(f"  Scope 1 Emissions (kg CO₂e): {scope1_emissions}")
        print(f"  Scope 2 Emissions (kg CO₂e): {scope2_emissions}")
        print(f"  Scope 3 Emissions (metric tonnes CO₂e): {scope3_emissions}")
        print(f"  Total Emissions (metric tonnes CO₂e): {rounded_emissions}")

    return monthly_emissions, annual_electricity, annual_water, annual_employee


def parse(string) -> list:
    strin = string.replace(" ", "")
    result = strin.split(",")
    return result
