from flask import Flask, session, redirect, render_template, request, url_for, g
import sqlite3
from models import calculate_carbon_footprint, parse
from werkzeug.security import generate_password_hash, check_password_hash
from utils import *
import numpy as np

app = Flask(__name__)
app.secret_key = "ABC123"

DATABASE = "Eco-Footprint-Analyzer/users/data.db"


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


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        hashed_password = generate_password_hash(password, method='sha256')

        db = get_db()
        cursor = db.cursor()
        cursor.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
                       (username, email, hashed_password))
        db.commit()

        return redirect("/login")
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()

        # Assuming password is the 4th column
        if user and check_password_hash(user[3], password):
            session['user_id'] = user[0]
            session['username'] = user[1]
            return redirect("/calculate")
        else:
            return "Invalid credentials. Please try again."

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('home'))


@app.route("/calculate", methods=["GET", "POST"])
def calculate():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == "POST":
        user_id = session['user_id']

        # Parse and validate input data
        try:
            electricity = np.array(
                [float(i) for i in parse(request.form.get("electricity"))])
            water = np.array([float(i)
                             for i in parse(request.form.get("water"))])
            employees = int(request.form.get("employees"))
            location = request.form.get("location")
            revenue = np.array([float(request.form.get("revenue"))])
            industry = request.form.get("industry")
        except (ValueError, TypeError) as e:
            return "Invalid input data. Please ensure all fields are correctly filled."

        # Calculate carbon footprint
        try:
            emissions, annual_electricity, annual_water, annual_employee = calculate_carbon_footprint(
                employees, electricity, water, revenue, industry, location
            )
        except Exception as e:
            return f"Error calculating carbon footprint: {e}"

        # Generate and save graphs
        try:
            e_bill_path = f"app/static/graphs/e-{user_id}.html"
            w_bill_path = f"app/static/graphs/w-{user_id}.html"
            rcf_path = f"app/static/graphs/rcf-{user_id}.html"
            emissions_bar_path = f"app/static/graphs/e-{user_id}.html"
            percentage_chart_path = f"app/static/graphs/p-{user_id}.html"

            ElectricityBill(electricity, user_id)
            WaterBill(water, user_id)
            RevenueToCF(revenue, emissions, np.array([industry]), user_id)
            EmissionsBar(emission=emissions, id=user_id)
            PercentageChart(
                annual_electricity=sum(annual_electricity),
                annual_water=sum(annual_water),
                annual_employee=sum(annual_employee),
                id=user_id
            )

            # Store graph file paths in the database
            db = get_db()
            cursor = db.cursor()
            cursor.execute('INSERT INTO graphs (id, file_location_1, file_location_2, file_location_3, file_location_4, file_location_5) VALUES (?, ?, ?, ?, ?, ?)',
                           (user_id, e_bill_path, w_bill_path, rcf_path, emissions_bar_path, percentage_chart_path))
            db.commit()

        except Exception as e:
            return f"Error generating graphs: {e}"

        return redirect("/history")

    return render_template("calculate.html")


@app.route("/history")
def history():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        'SELECT file_location_1, file_location_2, file_location_3, file_location_4, file_location_5 FROM graphs WHERE id = ?', (user_id,))
    graphs = cursor.fetchone()

    if graphs:
        graphs_list = list(graphs)
    else:
        graphs_list = []

    return render_template("history.html", graphs=graphs_list)


if __name__ == "__main__":
    app.run(debug=True)
