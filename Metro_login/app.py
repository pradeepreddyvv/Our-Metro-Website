import psycopg2  # pip install psycopg2
import re
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2.extras
from flask import Flask, request, session, redirect, url_for, render_template, flash
from flask import Flask, render_template, request, flash
# generate random integer values
from random import randint


# from flask_sqlalchemy import SQLAlchemy

# app = Flask(__name__)


# app.py

app = Flask(__name__)
app.secret_key = 'hi'

DB_HOST = "localhost"
DB_NAME = "metro10"
DB_USER = "postgres"
DB_PASS = "2000"

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER,
                        password=DB_PASS, host=DB_HOST)
print("hiiii")
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:2000@localhost/flasksql'
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# app.secret_key = 'hi'

# db = SQLAlchemy(app)


@app.route('/')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('home.html', name=session['name'])
    # User is not loggedin redirect to login page
    return redirect(url_for('main'))


@app.route('/payment')
def payment():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        # cursor.execute(
        #     'SELECT * FROM payment WHERE email_id = %s', (session['email_id'],))
        cursor.execute(
            'SELECT * FROM payment INNER JOIN metro_card ON payment.card_id=metro_card.card_id WHERE metro_card.card_id = (SELECT card_id FROM metro_card WHERE email_id= %s)', (session['email_id'],))
        # Fetch one record and return result
        payment = cursor.fetchone()
        print(payment)
        print(payment['status'])
        return render_template('payment.html', name=session['name'], status=payment['status'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/login/', methods=['GET', 'POST'])
def login():

    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    # Check if "email_id" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'email_id' in request.form and 'password' in request.form:
        email_id = request.form['email_id']
        password = request.form['password']
        print(password)

        # Check if account exists using MySQL
        cursor.execute(
            'SELECT * FROM members WHERE email_id = %s', (email_id,))
        # Fetch one record and return result
        account = cursor.fetchone()
        print(account)
        print(account['name'])

        if account:
            # print("user typed = ", password)
            password_rs = account['password']
            print(password_rs)
            # If account exists in users table in out database
            if password_rs == password:
                # if check_password_hash(password_rs, password):
                #     admin_email_account = cursor.execute(
                #         'SELECT * FROM admins WHERE email_id = %s', (email_id))
                #     if admin_email_account:
                #         # Create session data, we can access this data in other routes
                #         session['loggedin'] = True
                #         session['id'] = account['id']
                #         session['email_id'] = account['email_id']
                #         # Redirect to home page
                #         return redirect(url_for('admin'))
                #     else:
                #         # Account doesnt exist or email_id/password incorrect
                #         flash('Incorrect inner email_id/password')
                # Create session data, we can access this data in other routes
                session['loggedin'] = True
                # session['metro_id'] = account['metro_id']
                session['email_id'] = account['email_id']
                session['name'] = account['name']
                # Redirect to home page
                return redirect(url_for('home'))
            else:
                # Account doesnt exist or email_id/password incorrect
                flash('Incorrect inner email_id/password')
        else:
            # Account doesnt exist or email_id/password incorrect
            flash('Incorrect email_id/password')

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():

    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    # Check if "email_id", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'email_id' in request.form and 'phone_number' in request.form and 'phone_number2' in request.form and 'gender' in request.form and 'password' in request.form:
        # Create variables for easy access
        fullname = request.form['fullname']
        email_id = request.form['email_id']
        password = request.form['password']
        phone_number = request.form['phone_number']
        phone_number2 = request.form['phone_number2']
        gender = request.form['gender']
        passwordopen = request.form['password']
        gender = "M"
        # id = 987099
        # phone_number = 12345

        # print(value)
        _hashed_password = generate_password_hash(password)

        # getMaxId = ('select max(id) from members = %s')
        cursor.execute('select max(card_id) from metro_card')
        card_id = cursor.fetchone()
        print("card_id 1st =", card_id)

        cursor.execute('select max(payment_id) from payment')
        payment_id = cursor.fetchone()
        print("payment_id 1st =", payment_id)

        # Check if account exists using MySQL
        cursor.execute(
            'SELECT * FROM members WHERE email_id = %s', (email_id,))
        account = cursor.fetchone()
        print("account = ", account)
        # cursor.execute(
        #     'SELECT * FROM members WHERE card_id = %s', (card_id,))
        # card_valid = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            flash('Account already exists!')
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email_id):
            flash('Invalid email address!')
        elif not re.match(r'[A-Za-z0-9]+', email_id):
            flash('email_id must contain only characters and numbers!')
        elif not email_id or not password or not email_id:
            flash('Please fill out the form!')
        # elif not card_valid:
        #     # Account doesnt exists and the form data is valid, now insert new account into users table
        #     cursor.execute("INSERT INTO users (email_id, fullname, passwordopen, phone_no, card_id) VALUES (%s,%s,%s,%d,%d)",
        #                    (email_id, fullname, passwordopen, phone_no, card_id))
        #     # cursor.execute("INSERT INTO users (email_id, fullname, password, passwordopen, p_no, card_id) VALUES (%s,%s,%s,%s,%d,%d)",
        #     #                (email_id, fullname, _hashed_password, passwordopen, p_no, card_id))
        #     conn.commit()
        #     flash('You have successfully registered!')
        else:
            # Account doesnt exists and the form data is valid, now insert new account into users table
            # card_id = (int(card_id))
            # y = ''.join(card_id)  # converting list into string
            y = ''.join(map(str, card_id))
            z = int(y)
            z = z + 1
            print("card_id 2nd =", card_id)

            yp = ''.join(map(str, payment_id))
            zp = int(yp)
            zp = zp + 1
            print("card_id 2nd =", payment_id)
            cursor.execute("INSERT INTO members (email_id, name, password, p_no,p_no2, gender) VALUES (%s,%s,%s,%s,%s)",
                           (email_id, fullname, passwordopen, phone_number, gender,))
            cursor.execute("INSERT INTO metro_card (card_id , balance ,start_station ,destination ,s_time ,d_time ,email_id) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                           (z, 150, 'st_01', 'st_01', '00:00:00', '00:00:00', email_id,))
            cursor.execute("INSERT INTO payment (payment_id , status ,card_id) VALUES (%s,%s,%s)",
                           (zp, "paid", card_id))
            cursor.execute("INSERT INTO phoneno (p_no , p_no2 ,email_id) VALUES (%s,%s,%s)",
                           (phone_number, phone_number2, email_id,))
            # cursor.execute("INSERT INTO users (email_id, fullname, password, passwordopen, p_no, card_id) VALUES (%s,%s,%s,%s,%d,%d)",
            #                (email_id, fullname, _hashed_password, passwordopen, p_no, card_id))
            conn.commit()
            flash('You have successfully registered!')
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        flash('Please fill out the form!')
    # Show registration form with message (if any)
    return render_template('register.html')


@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    # session.pop('id', None)
    session.pop('email_id', None)
    session.pop('name', None)
    # Redirect to login page

    return redirect(url_for('login'))


@app.route('/profile')
def profile():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    # Check if user is loggedin
    if 'loggedin' in session:
        cursor.execute('SELECT * FROM members WHERE email_id = %s',
                       [session['email_id']])
        account = cursor.fetchone()
        # Show the profile page with account info
        return render_template('profile.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/main')
def main():

    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    # Check if user is loggedin
    # if 'loggedin' in session:
    # cursor.execute('SELECT * FROM users WHERE gender = %s',
    #                [session['email_id']])
    # account = cursor.fetchone()
    # Show the profile page with account info
    # return render_template('profile.html', account=account)
    # User is not loggedin redirect to login page
    # return redirect(url_for('login'))
    # if 'loggedin' in session:
    #     cursor.execute('select * from metro_card WHERE email_id= %s',
    #                    (session['email_id'],))
    #     metro_card = cursor.fetchone()
    #     print("metro_card 1st =", metro_card)
    # Check if "email_id", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'start' in request.form and 'dest' in request.form and 'gender' in request.form:
        # Create variables for easy access
        # fullname = request.form['fullname']
        start = request.form['start']
        dest = request.form['dest']
        gender = request.form['gender']
        # passwordopen = request.form['password']
        # user_id = 10002
        # phone_number = 12345

        # print(value)
        # _hashed_password = generate_password_hash(password)
        cursor.execute('select max(user_id) from users')
        user_id = cursor.fetchone()
        print("user_id 1st =", user_id)

        cursor.execute('select max(ticket_id) from ticket')
        ticket_id = cursor.fetchone()
        print("ticket_id 1st =", ticket_id)

        from datetime import datetime

        now = datetime.now()

        current_time = now.strftime("%H:%M:%S")
        print("Current Time =", current_time)

        if not start or not dest or not gender:
            flash('inner Please fill out the form!')
        else:
            # Account doesnt exists and the form data is valid, now insert new account into users table
            y = ''.join(map(str, user_id))
            z = int(y)
            z = z + 1
            print("card_id 2nd =", user_id)
            user_id = z

            yt = ''.join(map(str, ticket_id))
            zt = int(yt)
            zt = zt + 1
            print("card_id 2nd =", ticket_id)
            ticket_id = zt

            num1 = int(start.split("_")[1])
            num2 = int(start.split("_")[1])
            fare = abs((num2-num1)*5)
            # print("point_id =", point_id)
            cursor.execute("INSERT INTO users (user_id, gender) VALUES (%s,%s)",
                           (user_id, gender,))
            cursor.execute("INSERT INTO ticket (ticket_id, start_time, fare, start_station, destination, user_id) VALUES (%s,%s,%s,%s,%s,%s)",
                           (ticket_id, current_time, fare, start, dest, user_id,))
            # cursor.execute("INSERT INTO users (email_id, fullname, password, passwordopen, p_no, card_id) VALUES (%s,%s,%s,%s,%d,%d)",
            #                (email_id, fullname, _hashed_password, passwordopen, p_no, card_id))

            conn.commit()
            flash('You have successfully registered!')
            return render_template('main.html', gender=gender, start=start, dest=dest)
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        flash('outer Please fill out the form!')
    # Show registration form with message (if any)
    return render_template('main.html')

    ##################################################


@app.route('/members', methods=['GET', 'POST'])
def members():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    # Check if user is loggedin
    if 'loggedin' in session:
        cursor.execute('SELECT * FROM members WHERE email_id = %s',
                       [session['email_id']])
        account = cursor.fetchone()
        cursor.execute('SELECT * FROM metro_card WHERE email_id = %s',
                       [session['email_id']])
        metrocard_info = cursor.fetchone()
        print("final balance=", metrocard_info['balance'])

        # Check if "email_id", "password" and "email" POST requests exist (user submitted form)
        if request.method == 'POST' and 'add_amount' in request.form:
            # Create variables for easy access
            # fullname = request.form['fullname']
            add_amount1 = request.form['add_amount']
            print("add_amount", add_amount1)
            z = metrocard_info['card_id']
            final_balance = metrocard_info['balance'] + int(add_amount1)
            start = metrocard_info['start_station']
            dest = metrocard_info['destination']
            s_time = metrocard_info['s_time']
            d_time = metrocard_info['d_time']
            email_id = metrocard_info['email_id']

            # cursor.execute("ALTER TABLE metro_card (balance) VALUES (%s)",
            #                (final_balance,))
            print("final balance =", final_balance)
            # cursor.execute(
            #     'SELECT * FROM metro_card WHERE email_id = %s', [session['email_id']])
            cursor.execute('UPDATE metro_card SET balance = %s  WHERE email_id =%s',
                           [final_balance, session['email_id']])
            conn.commit()

        # Show the profile page with account info
        return render_template('members.html', account=account, metrocard_info=metrocard_info)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    # Check if "email_id", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'email_id' in request.form and 'phone_number' in request.form and 'phone_number2' in request.form and 'gender' in request.form and 'password' in request.form:
        # Create variables for easy access
        fullname = request.form['fullname']
        email_id = request.form['email_id']
        password = request.form['password']
        phone_number = request.form['phone_number']
        phone_number2 = request.form['phone_number2']
        gender = request.form['gender']
        passwordopen = request.form['password']
        # gender = "M"
        # id = 987099
        # phone_number = 12345

        # print(value)
        _hashed_password = generate_password_hash(password)

        # getMaxId = ('select max(id) from members = %s')
        cursor.execute('select max(card_id) from metro_card')
        card_id = cursor.fetchone()
        print("card_id 1st =", card_id)

        cursor.execute('select max(payment_id) from payment')
        payment_id = cursor.fetchone()
        print("payment_id 1st =", payment_id)

        # Check if account exists using MySQL
        cursor.execute(
            'SELECT * FROM members WHERE email_id = %s', (email_id,))
        account = cursor.fetchone()
        print("account = ", account)
        # cursor.execute(
        #     'SELECT * FROM members WHERE card_id = %s', (card_id,))
        # card_valid = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            flash('Account already exists!')
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email_id):
            flash('Invalid email address!')
        elif not re.match(r'[A-Za-z0-9]+', email_id):
            flash('email_id must contain only characters and numbers!')
        elif not email_id or not password or not email_id:
            flash('Please fill out the form!')
        # elif not card_valid:
        #     # Account doesnt exists and the form data is valid, now insert new account into users table
        #     cursor.execute("INSERT INTO users (email_id, fullname, passwordopen, phone_no, card_id) VALUES (%s,%s,%s,%d,%d)",
        #                    (email_id, fullname, passwordopen, phone_no, card_id))
        #     # cursor.execute("INSERT INTO users (email_id, fullname, password, passwordopen, p_no, card_id) VALUES (%s,%s,%s,%s,%d,%d)",
        #     #                (email_id, fullname, _hashed_password, passwordopen, p_no, card_id))
        #     conn.commit()
        #     flash('You have successfully registered!')
        else:
            # Account doesnt exists and the form data is valid, now insert new account into users table
            # card_id = (int(card_id))
            # y = ''.join(card_id)  # converting list into string
            y = ''.join(map(str, card_id))
            z = int(y)
            z = z + 1
            print("card_id 2nd =", card_id)

            yp = ''.join(map(str, payment_id))
            zp = int(yp)
            zp = zp + 1
            print("card_id 2nd =", payment_id)
            cursor.execute("INSERT INTO members (email_id, name, password, p_no,p_no2, gender) VALUES (%s,%s,%s,%s,%s)",
                           (email_id, fullname, passwordopen, phone_number, gender,))
            cursor.execute("INSERT INTO metro_card (card_id , balance ,start_station ,destination ,s_time ,d_time ,email_id) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                           (z, 150, 'st_01', 'st_01', '00:00:00', '00:00:00', email_id,))
            cursor.execute("INSERT INTO payment (payment_id , status ,card_id) VALUES (%s,%s,%s)",
                           (zp, "paid", card_id))
            cursor.execute("INSERT INTO phoneno (p_no , p_no2 ,email_id) VALUES (%s,%s,%s)",
                           (phone_number, phone_number2, email_id,))
            # cursor.execute("INSERT INTO users (email_id, fullname, password, passwordopen, p_no, card_id) VALUES (%s,%s,%s,%s,%d,%d)",
            #                (email_id, fullname, _hashed_password, passwordopen, p_no, card_id))
            conn.commit()
            flash('You have successfully registered!')
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        flash('Please fill out the form!')
    return render_template('admin.html', email_id=session['email_id'])


@app.route('/bookings', methods=['GET', 'POST'])
def bookings():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if 'loggedin' in session:
        cursor.execute('select * from metro_card WHERE email_id= %s',
                       (session['email_id'],))
        metro_card = cursor.fetchone()
        print("metro_card 1st =", metro_card)
    # Check if "email_id", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'start' in request.form and 'dest' in request.form and 'gender' in request.form:
        # Create variables for easy access
        # fullname = request.form['fullname']
        start = request.form['start']
        dest = request.form['dest']
        gender = request.form['gender']
        # passwordopen = request.form['password']
        # user_id = 10002
        # phone_number = 12345

        # print(value)
        # _hashed_password = generate_password_hash(password)
        cursor.execute('select max(user_id) from users')
        user_id = cursor.fetchone()
        print("user_id 1st =", user_id)

        cursor.execute('select max(ticket_id) from ticket')
        ticket_id = cursor.fetchone()
        print("ticket_id 1st =", ticket_id)

        from datetime import datetime

        now = datetime.now()

        current_time = now.strftime("%H:%M:%S")
        print("Current Time =", current_time)

        if not start or not dest or not gender:
            flash('inner Please fill out the form!')
        else:
            # Account doesnt exists and the form data is valid, now insert new account into users table
            y = ''.join(map(str, user_id))
            z = int(y)
            z = z + 1
            print("card_id 2nd =", user_id)
            user_id = z

            yt = ''.join(map(str, ticket_id))
            zt = int(yt)
            zt = zt + 1
            print("card_id 2nd =", ticket_id)
            ticket_id = zt

            num1 = int(start.split("_")[1])
            num2 = int(dest.split("_")[1])
            fare = abs((num2-num1)*5)
            print(num1)
            print(num2)
            print(fare)
            # print("point_id =", point_id)
            cursor.execute("INSERT INTO users (user_id, gender) VALUES (%s,%s)",
                           (user_id, gender,))
            conn.commit()
            cur = cursor.execute("INSERT INTO ticket (ticket_id, start_time, fare, start_station, destination, user_id) VALUES (%s,%s,%s,%s,%s,%s)",
                                 (ticket_id, current_time, fare, start, dest, user_id,))
            # cursor.execute("INSERT INTO users (email_id, fullname, password, passwordopen, p_no, card_id) VALUES (%s,%s,%s,%s,%d,%d)",
            #                (email_id, fullname, _hashed_password, passwordopen, p_no, card_id))

            conn.commit()
            flash('You have successfully registered!')
            return render_template('bookings.html', start=start, dest=dest)
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        flash('outer Please fill out the form!')
    # Show registration form with message (if any)
    return render_template('bookings.html')


if __name__ == "__main__":
    app.run(debug=True)
