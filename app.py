from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from datetime import datetime  # Import datetime module for date and time conversion

app = Flask(__name__)

# MySQL database connection
try:
    db = mysql.connector.connect(
        host="care-4-u.c5eyis2co1ux.ap-south-1.rds.amazonaws.com",  # replace with your MySQL host
        user="root",  # replace with your MySQL username
        password="Health-care-4-u",  # replace with your MySQL password
        database="care"  # replace with your database name
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
        department = request.form.get('department')
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

        # Insert appointment details into the database
        try:
            query = "INSERT INTO appointments (department, doctor, name, email, date, time) VALUES (%s, %s, %s, %s, %s, %s)"
            values = (department, doctor, name, email, formatted_date, formatted_time)
            cursor.execute(query, values)
            db.commit()
        except mysql.connector.Error as err:
            return f"Error: {err}"
        finally:
            cursor.close()

        return redirect(url_for('appointment'))

if __name__ == "__main__":
    app.run(debug=True)
