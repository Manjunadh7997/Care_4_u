from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from datetime import datetime  # Import datetime module for date and time conversion
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER") 
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB = os.getenv("DB")


#print(f"DB_HOST: {DB_HOST}, DB_USER: {DB_USER}, DB_PASSWORD: {DB_PASSWORD}, DB: {DB}")  # Debugging line to check if environment variables are loaded correctly
# MySQL database connection
try:
    db = mysql.connector.connect(
        host= DB_HOST,  # replace with your MySQL host
        user= DB_USER,  # replace with your MySQL username
        password= DB_PASSWORD,  # replace with your MySQL password
        database= DB  # replace with your database name
    )
    cursor = db.cursor()
except mysql.connector.Error as err:
    print(f"Error: {err}")
    exit(1)

# Route to render the index page
@app.route('/')
def index():
    return render_template('index.html')

# Route to render the appointment page
@app.route('/appointment')
def appointment():
    return render_template('appointment.html')

# Route to render the about page
@app.route("/about")
def about():
    return render_template("about.html")

# Route to render the service page
@app.route("/service")
def service():
    return render_template("service.html")

# Route to render the team page
@app.route("/team")
def team():
    return render_template("team.html")

# Route to render the contact page
@app.route("/contact")
def contact():
    return render_template("contact.html")

# Route to handle form submission
@app.route('/submit', methods=['POST'])
def submit_appointment():
    if request.method == 'POST':
        department = request.form.get('department').strip()  # Remove any extra spaces
        doctor = request.form.get('doctor')
        name = request.form.get('name')
        email = request.form.get('email')
        date = request.form.get('date')
        time = request.form.get('time')
        
        # Convert date from MM/DD/YYYY to YYYY-MM-DD format
        try:
            date_obj = datetime.strptime(date, "%m/%d/%Y")
            formatted_date = date_obj.strftime("%Y-%m-%d")
        except ValueError:
            return "Invalid date format. Please use MM/DD/YYYY."

        # Convert time from h:mm AM/PM to HH:MM:SS format
        try:
            time_obj = datetime.strptime(time, "%I:%M %p")
            formatted_time = time_obj.strftime("%H:%M:%S")
        except ValueError:
            return "Invalid time format. Please use h:mm AM/PM."

        # Map departments to table names
        department_tables = {
            "Emergency Care": "emergency_care_appointments",
            "Operation and Surgery": "operation_surgery_appointments",
            "Outdoor Checkup": "outdoor_checkup_appointments",
            "General Check up": "general_checkup_appointments",
            "Full body check up": "full_body_checkup_appointments",
            "Blood Testing": "blood_testing_appointments"
        }

        table_name = department_tables.get(department)

        # Check if department is valid
        if not table_name:
            return "Invalid department selected."

        # Ensure the department-specific table exists
        try:
            with db.cursor() as cursor:
                create_table_query = f"""
                CREATE TABLE IF NOT EXISTS {table_name} (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    doctor VARCHAR(255),
                    name VARCHAR(255),
                    email VARCHAR(255),
                    date DATE,
                    time TIME
                );
                """
                cursor.execute(create_table_query)
                db.commit()  # Ensure the table creation is committed
        except mysql.connector.Error as err:
            return f"Error creating table for department: {err}"

        # Insert appointment details into the department-specific table
        try:
            with db.cursor() as cursor:
                insert_query = f"INSERT INTO {table_name} (doctor, name, email, date, time) VALUES (%s, %s, %s, %s, %s)"
                values = (doctor, name, email, formatted_date, formatted_time)
                cursor.execute(insert_query, values)
                db.commit()
        except mysql.connector.Error as err:
            return f"Error inserting appointment: {err}"

        # Redirect to the appointment confirmation page with appointment details
        return redirect(url_for('appointment_booked', name=name, doctor=doctor, department=department, date=formatted_date, time=formatted_time))

# Route to render the appointment booked page
@app.route('/appointment_booked')
def appointment_booked():
    name = request.args.get('name')
    doctor = request.args.get('doctor')
    department = request.args.get('department')
    date = request.args.get('date')
    time = request.args.get('time')
    
    return render_template('appointment_booked.html', name=name, doctor=doctor, department=department, date=date, time=time)

if __name__ == "__main__":
    port = int(
        os.getenv("PORT", 8000)
    )

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
