from flask import Flask, session, redirect, render_template, request, url_for, g
import sqlite3
from models import calculate_carbon_footprint, parse
from werkzeug.security import generate_password_hash, check_password_hash
from utils import *
import numpy as np

app = Flask(__name__)
app.secret_key = "ABC123"

DATABASE = "C:/Users/Lenovo/Documents/Code/projects/Ecometer/users/data.db"


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("nameSignup")
        email = request.form.get("emailSignup")
        password = request.form.get("passwordSignup")
        hashed_password = generate_password_hash(
            password, method='pbkdf2:sha256')

        db = get_db()
        cursor = db.cursor()
        cursor.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
                       (username, email, hashed_password))
        db.commit()

        return redirect("/signin")
    return render_template("signup.html")


@app.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        email = request.form.get("emailSignin")
        password = request.form.get("passwordSignin")

        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()

        if user and check_password_hash(user[3], password):
            session['user_id'] = user[0]
            session['username'] = user[1]
            return redirect("/calculate")
        else:
            return "Invalid credentials. Please try again."

    return render_template("signin.html")


@app.route("/logout")
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('home'))


@app.route("/calculate", methods=["GET", "POST"])
def calculate():
    if 'user_id' not in session:
        return redirect(url_for('signin'))

    if request.method == "POST":
        user_id = session['user_id']
        try:
            # Retrieve and parse form data
            employeeCount = float(request.form.get("employeeCount"))
            electricityUsage = [float(x) for x in parse(
                request.form.get("electricityUsage"))]
            waterUsage = [float(x)
                          for x in parse(request.form.get("waterUsage"))]
            revenue = float(request.form.get("revenue"))
            industry = request.form.get("industry")
            country = request.form.get("country")

            print(employeeCount, electricityUsage,
                  waterUsage, revenue, industry, country)
            print(type(employeeCount), type(electricityUsage), type(
                waterUsage), type(revenue), type(industry), type(country))

        except (ValueError, TypeError) as e:
            print(f"Error in input data parsing: {e}")
            return render_template("calculate.html", error="Invalid input data. Please ensure all fields are correctly filled.")

        # Calculate carbon footprint
        try:
            emissions, annual_electricity, annual_water, annual_employee = calculate_carbon_footprint(
                employee_count=employeeCount,
                electricity_usage=electricityUsage,
                water_usage=waterUsage,
                revenue=revenue,
                industry=industry,
                location=country
            )
            print("Calculated Emissions: ", emissions)
            print("Annual Electricity Emissions: ", annual_electricity)
            print("Annual Water Emissions: ", annual_water)
            print("Annual Employee Emissions: ", annual_employee)

        except Exception as e:
            print(f"Error calculating carbon footprint: {e}")
            return render_template("calculate.html", error=f"Error calculating carbon footprint: {e}")

        # Store and visualize data
        try:
            ElectricityBill(electricityUsage, ide=user_id)
            WaterBill(waterUsage, ide=user_id)
            EmissionsBar(emission=emissions, ide=user_id)
            PercentageChart(
                Employee_Emissions=sum(annual_employee),
                Electricity_Emissions=sum(annual_electricity),
                Water_Emissions=sum(annual_water),
                ide=user_id
            )
            print("Emissions stored and charts generated")

        except Exception as e:
            print(f"Error generating graphs: {e}")
            return render_template("calculate.html", error=f"Error generating graphs: {e}")

        return render_template("calculate.html", idd=user_id, success="Calculation successful")

    return render_template("calculate.html")


@app.route("/history")
def history():
    return render_template("history.html")


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)
