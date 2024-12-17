from binascii import Error
from flask import Flask, jsonify, render_template, request
from flask import Flask, render_template, request, redirect, url_for, session ,flash
from dbconnection import get_db_connection
# import mysql.connector
import threading

import os




app = Flask(__name__)
app.secret_key = 'a8f5f167f44f4964e6c998dee827110c' 







@app.route('/')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template("signup.html")


#route for sign up user

@app.route('/signup_user', methods=['GET', 'POST'])
def signup_user():
    if request.method == 'POST':
        fullname = request.form.get('fullname')
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Input validation
        if password != confirm_password:
            flash("Passwords do not match!", "error")
            return render_template('signup.html')

        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            # Check if username or email already exists
            cursor.execute("SELECT * FROM users WHERE user_name = %s OR email = %s", (username, email))
            user_exists = cursor.fetchone()

            if user_exists:
                flash("Username already exists!", "error")
                return render_template('signup.html')
            
            cursor.execute("SELECT * FROM users WHERE email = %s", (email))
            user_email = cursor.fetchone()

            if user_email:
                flash("email aderss already exists!", "error")
                return render_template('signup.html')

            # Insert new user into the database
            query = "INSERT INTO users (name, email, user_name, password) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (fullname, email, username, password))
            connection.commit()

            flash("Account created successfully! Please log in.", "success")
            return redirect('/')  # Redirect to the login page

        except OSError as err:
            print(f"Error: {err}")
            flash("An error occurred. Please try again later.", "error")
            return render_template('signup.html')

        finally:
            cursor.close()
            connection.close()

    # Render the signup form for GET requests
    return render_template('login.html')



#route for user_login
@app.route('/login_user', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username =='chetan@123' and password == 'Pass@1234':
            return render_template('admin.html')
            
        



        connection = get_db_connection()
        cursor = connection.cursor()

        try:
            # connection = get_db_connection()
            # cursor = connection.cursor(dictionary=True)

            # Query the database for the user by username
            cursor.execute("SELECT * FROM users WHERE user_name = %s", (username,))
            user = cursor.fetchone()

            if user:
                # Check if the provided password matches the hashed password in the database
                # if bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
                    # User is authenticated, create a session
                if  password == user[4]:
                    session['user_id'] = user[0]
                    session['username'] = user[3]
                    # "Login successful!", "success")
                    name = user[1]
                    return redirect('/home' )  # Redirect to the home page or a dashboard
                else:
                    flash("Incorrect password. Please try again.", "error")
                    return redirect('/')  # Reload login page
            else:
                flash("Username not found. Please try again.", "error")
                return redirect('/')  # Reload login page

        except OSError as err:
            print(f"Error: {err}")
            flash("An error occurred. Please try again later.", "error")
        
        finally:
            cursor.close()
            connection.close()

    return render_template('login.html')



# Route for the Home Page
@app.route('/home')
def home():

    # username= session['usersname'] 
    
    return render_template('home.html')







# Route for search results
@app.route('/search_buses', methods=['GET'])
def search():
    source = request.args.get('from')
    destination = request.args.get('to')
    date = request.args.get('date')
    
    
    connection = get_db_connection()
    cursor = connection.cursor()
    # sql = "SELECT * FROM buses WHERE source = %s AND destination = %s " 
    # val = ("pune", "mumbai")  
    
    query = "SELECT * FROM buses WHERE d_loction = %s AND a_location = %s AND d_dt >= %s  "
          
    cursor.execute(query, (source, destination, date))
    
    try:
       
        
        buses = cursor.fetchall() 
        
        
    except Exception as e:
        print(f"An error occurred: {e}")
        return e
          
    finally:
        cursor.close()
        connection.close()
    
    return render_template('search_results.html', buses=buses)




# @app.route('/booking1/<int:bus_id>')
# def booking1(bus_id):

    # username= session['usersname']

    connection = get_db_connection()
    cursor = connection.cursor()
    # sql = "SELECT * FROM buses WHERE source = %s AND destination = %s " 
    # val = ("pune", "mumbai")  
    
    query = "SELECT * FROM buses WHERE d_loction = %s AND a_location = %s AND d_dt >= %s  "
          
    cursor.execute(query, (source, destination, date))
    
    try:
       
        
        buses = cursor.fetchall() 
        
        
    except Exception as e:
        print(f"An error occurred: {e}")
        return e
          
    finally:
        cursor.close()
        connection.close()
    
    return render_template('search_results.html', buses=buses)



#it goto passenger page
@app.route('/booking1/<int:bus_id>')
def booking1(bus_id):

    bus_id = bus_id

    connection = get_db_connection()
    cursor = connection.cursor()
    # sql = "SELECT * FROM buses WHERE source = %s AND destination = %s " 
    # val = ("pune", "mumbai")  
    
    query = "SELECT price FROM buses WHERE bus_id = %s  "
          
    cursor.execute(query,bus_id)
    
    try:
       
        
         result = cursor.fetchone() 
        
        
    except Exception as e:
        print(f"An error occurred: {e}")
        return e
          
    finally:
        cursor.close()
        connection.close()

    
    price = float(result[0])
    print(price)
    
    return render_template('passenget.html', price = price, bus_id = bus_id)




# @app.route('/save_booking', methods=['POST'])
# def save_passenger_details():



    try:
        # Fetch data from the form
        data = request.json
        bus_id = data['bus_id']
        travel_date = data['travel_date']
        departure_time = data['departure_time']
        total_price = data['total_price']
        passengers = data['passengers']

        connection = get_db_connection()
        cursor = connection.cursor()

        # Insert booking data
        cursor.execute("""
            INSERT INTO bookings (user_id, bus_id, travel_date, departure_time, total_price)
            VALUES (%s, %s, %s, %s, %s)
        """, (1, bus_id, travel_date, departure_time, total_price))
        booking_id = cursor.lastrowid

        # Insert passenger data
        for passenger in passengers:
            cursor.execute("""
                INSERT INTO passengers (booking_id, name, age, gender)
                VALUES (%s, %s, %s, %s)
            """, (booking_id, passenger['name'], passenger['age'], passenger['gender']))

        connection.commit()
        return jsonify({'status': 'success', 'booking_id': booking_id})

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})


@app.route('/save_booking', methods=['POST'])
def save_booking():
    # if 'user_id' not in session:
    #     return redirect(url_for('login'))  # Redirect to login if not logged in
    

    # data = request.json
    # tiprice = data.get('totalPriceEl')
    # print(tiprice)

    if request.method == 'POST':
        # Process booking form submission
        user_id = session['user_id']
        bus_id = request.form.get('bus_id')
        passengers = []

        passenger_names = request.form.getlist('name')
        passenger_ages = request.form.getlist('age')
        passenger_genders = request.form.getlist('gender')

        for name, age, gender in zip(passenger_names, passenger_ages, passenger_genders):
            passengers.append({
                'name': name,
                'age': int(age),
                'gender': gender
            })

        # Save booking and passenger details in the database
        try:
            connection = get_db_connection()
            cursor = connection.cursor()

            # Insert booking record with bus_id
            booking_query = "INSERT INTO bookings (user_id, bus_id) VALUES (%s, %s)"
            cursor.execute(booking_query, (user_id, bus_id))
            booking_id = cursor.lastrowid

            # Insert passenger records
            passenger_query = """
                INSERT INTO passengers (booking_id, user_id, name, age, gender)
                VALUES (%s, %s, %s, %s, %s)
            """
            for passenger in passengers:
                cursor.execute(passenger_query, (booking_id, user_id, passenger['name'], passenger['age'], passenger['gender']))

            # Update available seats for the bus
            update_seats_query = "UPDATE buses SET available_seats = available_seats - %s WHERE bus_id = %s"
            cursor.execute(update_seats_query, (len(passengers), bus_id))

            get_bus = "select * from buses where bus_id = %s"
            cursor.execute(get_bus, bus_id)
            bus = cursor.fetchone() 


            connection.commit()
        except Error as err:
            print(f"Database Error: {err}")
            return "An error occurred while processing your booking."
        finally:
            cursor.close()
            connection.close()

        return render_template("confirmation.html",booking_id = booking_id, bus = bus, passengers = passengers)

    
        

@app.route('/mybooking')
def mybooking():
    try:
            connection = get_db_connection()
            cursor = connection.cursor()

            id = session['user_id']
            print(id)


            # Insert booking record with bus_id
            query = "select * from bookings where user_id = %s  "
            cursor.execute(query, id)
            booking_id = cursor.fetchall() 


            query2 = "select * from passengers where user_id = %s "
            cursor.execute(query2, id)
            ipassengers = cursor.fetchall() 



           

    except Error as err:
        print(f"Database Error: {err}")
        return "An error occurred while processing your booking."
    finally:
        cursor.close()
        connection.close()


    return render_template("Mybooking.html",bookings = booking_id, passengers = ipassengers)






# @app.route('/payment')
# def payment():
#     booking_id = request.args.get('booking_id')
    
#     # Fetch booking details using booking_id
#     connection = get_db_connection()
#     cursor = connection.cursor()
#     cursor.execute("""
#         SELECT * FROM bookings WHERE booking_id = %s
#     """, (booking_id,))
#     booking = cursor.fetchone()

#     # Fetch passenger details
#     cursor.execute("""
#         SELECT * FROM passengers WHERE booking_id = %s
#     """, (booking_id,))
#     passengers = cursor.fetchall()

#     return render_template('payment.html', booking=booking, passengers=passengers)











@app.route('/logout')
def logout():
    # Clear the session to log the user out
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for('login'))







if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000,debug=True)
   