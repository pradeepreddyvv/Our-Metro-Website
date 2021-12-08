import psycopg2  # pip install psycopg2
import re
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2.extras
from flask import Flask, request, session, redirect, url_for, render_template, flash
from flask import Flask, render_template, request, flash
# generate random integer values
from random import randint
from datetime import datetime
# import datetime
import datetime as dt


# from flask_sqlalchemy import SQLAlchemy

# app = Flask(__name__)


# app.py

app = Flask(__name__)
app.secret_key = 'hi'

DB_HOST = "localhost"
DB_NAME = "metro11"
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
    platform = []
    return redirect(url_for('main', platform=platform))


@app.route('/payment')
def payment():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        # cursor.execute(
        #     'SELECT * FROM payment WHERE email_id = %s', (session['email_id'],))
        payment = cursor.execute(
            'SELECT status FROM payment INNER JOIN metro_card ON payment.card_id=metro_card.card_id WHERE metro_card.card_id = (SELECT card_id FROM metro_card WHERE email_id= %s)', (session['email_id'],))
        # Fetch one record and return result
        status = cursor.fetchone()
        print(session['email_id'])
        # print(payment)
        # print(str(payment['status']))
        return render_template('payment.html', name=session['name'], status=status)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/login/', methods=['GET', 'POST'])
def login():
    # cursor = conn.cursor()
    # cursor.execute("ROLLBACK")
    # conn.commit()

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
        cursor.execute(
            'SELECT * FROM metro_card WHERE email_id = %s', (email_id,))
        # Fetch one record and return result
        metro_card = cursor.fetchone()
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
                session['start_station'] = metro_card['start']
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
        # gender = "M"
        # id = 987099
        # phone_number = 12345

        # print(value)
        _hashed_password = generate_password_hash(password)

        # getMaxId = ('select max(id) from members = %s')
        cursor = conn.cursor()
        cursor.execute("ROLLBACK")
        conn.commit()
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

            # now = datetime.now()

            # current_time = now.strftime("%H:%M:%S")
            # print("Current Time =", current_time)

            current_time = dt.datetime.now()  # or dt.datetime.now(dt.timezone.utc)
            dest_time = current_time + dt.timedelta(seconds=1000)

            # get '14:39:57':
            a = dest_time.strftime('%H:%M:%S')
            print(a)
            current_time = current_time.strftime('%H:%M:%S')
            print(current_time)
            cursor.execute("INSERT INTO members (email_id, name, gender, password) VALUES (%s,%s,%s,%s)",
                           (email_id, fullname, gender, passwordopen,))
            cursor.execute("INSERT INTO metro_card (card_id , balance ,start ,destination ,s_time ,d_time ,email_id) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                           (z, 150, 'st_01', 'st_01', current_time, current_time, email_id,))
            cursor.execute("INSERT INTO payment (payment_id , status ,card_id) VALUES (%s,%s,%s)",
                           (zp, "paid", z))
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
    session.pop('start_station', None)
    session.pop('email_id', None)
    session.pop('name', None)
    cursor = conn.cursor()
    cursor.execute("ROLLBACK")
    conn.commit()
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
        cursor.execute('SELECT * FROM phoneno WHERE email_id = %s',
                       [session['email_id']])
        phoneno = cursor.fetchone()
        # Show the profile page with account info
        return render_template('profile.html', account=account, phoneno1=phoneno['p_no'], phoneno2=phoneno['p_no2'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/report', methods=['GET', 'POST'])
def report():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    # Check if user is loggedin
    if 'loggedin' in session:
        cursor.execute('SELECT * FROM members WHERE email_id = %s',
                       [session['email_id']])
        account = cursor.fetchone()
        cursor.execute('SELECT * FROM phoneno WHERE email_id = %s',
                       [session['email_id']])
        phoneno = cursor.fetchone()
        # Show the profile page with account info
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        if request.method == 'POST' and 'subject' in request.form and 'report_con' in request.form:
            # Create variables for easy access
            # fullname = request.form['fullname']
            subject = request.form['subject']
            report_content = request.form['report_con']
            cursor.execute("INSERT INTO report (report_subject , report ,email_id) VALUES (%s,%s,%s)",
                           (subject, report_content, session['email_id'],))
            conn.commit()
            flash('You have successfully reported!')
            return render_template('report.html', account=account, phoneno1=phoneno['p_no'], phoneno2=phoneno['p_no2'])
        elif request.method == 'POST':
            # Form is empty... (no POST data)
            flash('outer Please fill out the form!')
        return render_template('report.html', account=account, phoneno1=phoneno['p_no'], phoneno2=phoneno['p_no2'])
    # User is not loggedin redirect to login page
    return render_template(url_for('login'))


@app.route('/main', methods=['GET', 'POST'])
def main():

    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    # if 'loggedin' in session:
    #     session.pop('loggedin', None)
    #     session.pop('start_station', None)
    #     session.pop('email_id', None)
    #     session.pop('name', None)
    #     cursor = conn.cursor()
    #     cursor.execute("ROLLBACK")
    #     conn.commit()

    if request.method == 'POST' and 'start' in request.form and 'dest' in request.form and 'gender' in request.form:
        # Create variables for easy access
        # fullname = request.form['fullname']
        start = request.form['start']
        dest = request.form['dest']
        gender = request.form['gender']

        cursor.execute('select max(user_id) from users')
        user_id = cursor.fetchone()
        print("user_id 1st =", user_id)

        cursor.execute('select max(ticket_id) from ticket')
        ticket_id = cursor.fetchone()
        print("ticket_id 1st =", ticket_id)

        cursor.execute(
            'select station_id from station WHERE station_name = %s', (start,))
        station_id = cursor.fetchone()
        print("station_id 1st =", station_id)

        now = datetime.now()
        now1 = dt.datetime.now()

        current_time = now.strftime("%H:%M:%S")
        print("Current Time =", current_time)

        if not start or not dest or not gender:
            flash('inner Please fill out the form!')
        elif start == dest:
            flash('Please fill out the form with correct station names!')
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

            st = ''.join(map(str, station_id))
            st1 = int(st)
            st1 = st1 + 1
            print("card_id 2nd =", station_id)
            station_id = st1

            num1 = int(start.split("_")[1])
            num2 = int(dest.split("_")[1])
            # fare = abs((num2-num1)*5)

            # start1 = int(start.split("_")[1])
            # dest1 = int(dest.split("_")[1])
            l1 = ["st_01", "st_02", "st_03", "st_04", "st_05", "st_06"]
            l2 = ["st_07", "st_08", "st_03", "st_09", "st_10", "st_11"]

            if(start in l1 and dest in l1):
                time_final = abs(num2 - num1)
                metro_id = 384951
            elif(start in l1 and dest in l2):
                start_index = l1.index(start)
                des_index = l2.index(dest)
                intersection1 = l1.index(list(set(l1) & set(l2))[0])
                intersection2 = l2.index(list(set(l1) & set(l2))[0])
                # print(intersection2)
                time_final = abs(des_index-intersection2) + \
                    abs(start_index-intersection1)
                # print(time_final)
                metro_id = 384951
            elif(start in l2 and dest in l1):
                start_index = l2.index(start)
                des_index = l1.index(dest)
                intersection1 = l1.index(list(set(l1) & set(l2))[0])
                intersection2 = l2.index(list(set(l1) & set(l2))[0])
                time_final = abs(des_index-intersection1) + \
                    abs(start_index-intersection2)
                metro_id = 384952
            else:
                start_index = l2.index(start)
                des_index = l2.index(dest)
                time_final = abs(des_index - start_index)
                metro_id = 384952
            print("\n\n\n ", time_final)
            fare = time_final*5

            today = datetime.today()
            print("Today's date:", today)
            today_date = today.strftime('%d:%m:%Y')
            current_time = dt.datetime.now()  # or dt.datetime.now(dt.timezone.utc)
            c_time = current_time.strftime('%H:%M:%S')
            dest_time = now + dt.timedelta(seconds=(time_final*600))
            d_time = dest_time.strftime('%H:%M:%S')
            print(c_time)
            print(d_time)
            print(dest_time)
            print(today_date)


# way
            st1_arr = [6, 5, 4, 3, 2, 1]
            st2_arr = [12, 11, 10, 9, 8, 7]
            time_line1 = [0, 5, 10, 15, 20, 25, 30, 35, 40,
                          45, 50, 55]  # 1 to 6 and 7 to 11 (-1)  5->25
            time_line2 = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55]
            if(start in l1):

                dest_time = now + dt.timedelta(seconds=(time_final*600))
                d_time = dest_time.strftime('%H:%M:%S')
                print(d_time)
                if((time_line1[num1-1]) >= now1.minute):
                    arr_t = time_line1[num1-1] - now1.minute
                else:
                    arr_t = time_line1[11-(num1-1)] - now1.minute
                # arr_t = (abs(num1-1))*5
                # arrival_time = ("%s:,%s:,%s", now1.hour, arr_t, now1.second)
                arrival_time = current_time + \
                    dt.timedelta(seconds=(arr_t*60))
                des_t = (abs(time_final))*5
                departure_time = arrival_time + \
                    dt.timedelta(seconds=(time_final*5*60))
                # waiting_time = arrival_time - current_time
            else:

                dest_time = now + dt.timedelta(seconds=(time_final*600))
                d_time = dest_time.strftime('%H:%M:%S')
                print(d_time)
                if((time_line1[num1-7]) >= now1.minute):
                    arr_t = time_line1[num1-7] - now1.minute
                else:
                    arr_t = time_line1[11-(num1-7)] - now1.minute
                # arr_t = (abs(num1-1))*5
                # arrival_time = ("%s:,%s:,%s", now1.hour, arr_t, now1.second)
                arrival_time = current_time + \
                    dt.timedelta(seconds=(arr_t*60))
                des_t = (abs(time_final))*5
                departure_time = arrival_time + \
                    dt.timedelta(seconds=(time_final*5*60))
                # waiting_time = dt.timedelta(
                #     arrival_time - current_time)

            print("final")
            waiting_time = arrival_time - current_time
            print(waiting_time)

            arrival_time = arrival_time.strftime('%H:%M')
            departure_time = departure_time.strftime('%H:%M')
            # waiting_time = waiting_time.strftime('%H:%M')

            print("\n arrival_time =", arrival_time)
            print("\n departure_time = ", departure_time)
            print("\n waiting_time = ", waiting_time)

            # arrival_time =
            # print("point_id =", point_id)

            cursor.execute("INSERT INTO users (user_id, gender, station_id) VALUES (%s,%s,%s)",
                           (user_id, gender, station_id,))
            cursor.execute("INSERT INTO ticket (ticket_id, date_cur , start_time, end_time, fare, start, destination, user_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
                           (ticket_id, today_date, c_time, departure_time, fare, start, dest, user_id,))
            cursor.execute("INSERT INTO platform (platform_no,arrival_time, departure_time, waiting_time, station_id, user_id) VALUES (%s,%s,%s,%s,%s,%s)",
                           (1, arrival_time, departure_time, waiting_time, station_id, user_id,))
            cursor.execute("INSERT INTO boards (metro_id, user_id, station_id) VALUES (%s,%s,%s)",
                           (metro_id, user_id, station_id,))
            conn.commit()
            cursor.execute(
                'select * from station WHERE station_name = %s', (start,))
            station = cursor.fetchone()
            cursor.execute(
                'select * from boards WHERE user_id = %s', (user_id,))
            boards = cursor.fetchone()
            cursor.execute(
                'select * from ticket WHERE user_id = %s', (user_id,))
            ticket = cursor.fetchone()
            cursor.execute(
                'select * from platform WHERE user_id = %s', (user_id,))
            platform = cursor.fetchone()
            print("platform       1st =", platform)
            conn.commit()

            flash('You have successfully booked!')

            return render_template('main.html',  station=station, boards=boards, platform=platform, gender=gender, ticket=ticket,)
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        flash('outer Please fill out the form!')
    # Show registration form with message (if any)
    return render_template('main.html')

    ##################################################


@ app.route('/members', methods=['GET', 'POST'])
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
        # waiting_time = metrocard_info['s_time'] - metrocard_info['d_time']
        cursor.execute('SELECT * FROM phoneno WHERE email_id = %s',
                       [session['email_id']])
        phoneno = cursor.fetchone()
        print("final balance=", metrocard_info['balance'])

        # Check if "email_id", "password" and "email" POST requests exist (user submitted form)
        if request.method == 'POST' and 'add_amount' in request.form:
            # Create variables for easy access
            # fullname = request.form['fullname']
            add_amount1 = request.form['add_amount']
            print("add_amount", add_amount1)
            z = metrocard_info['card_id']
            final_balance = metrocard_info['balance'] + int(add_amount1)
            start = metrocard_info['start']
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
        return render_template('members.html', account=account, metrocard_info=metrocard_info, phoneno=phoneno)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/bookings', methods=['GET', 'POST'])
def bookings():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    current_time = dt.datetime.now()  # or dt.datetime.now(dt.timezone.utc)
    c_time = current_time.strftime('%H:%M:%S')
    # c_time = current_time.strftime('%H:%M')
    if 'loggedin' in session:
        # cursor = conn.cursor()
        # cursor.execute("ROLLBACK")
        # conn.commit()
        cursor.execute(
            'select * from metro_card WHERE email_id= %s', (session['email_id'],))
        metro_card = cursor.fetchone()
        cursor.execute('SELECT * FROM metro_card WHERE email_id = %s',
                       [session['email_id']])
        metrocard_info = cursor.fetchone()
        # waiting_time = metrocard_info[4] - c_time
        # print("metro_card 1st =", metro_card)
        # start = metro_card['start']
        # now = datetime.now()

        now1 = dt.datetime.now()

        current_time = now1.strftime("%H:%M:%S")
        print("Current Time =", current_time)
        cu_H = int(now1.strftime("%H"))
        cu_M = int(now1.strftime("%M"))
        s_t_H = int(metrocard_info['s_time'].split(":")[0])
        s_t_M = int(metrocard_info['s_time'].split(":")[1])
        wait_H = s_t_H - cu_H
        wait_M = s_t_M - cu_M
        print("final")
        if(wait_H >= 0 and wait_M >= 0):
            waiting_time = (str)(wait_H) + ":"+(str)(wait_M)
            print("waiting_time =", waiting_time)
        else:
            waiting_time = "boarded"
        cursor.execute(
            'select * from station WHERE station_name = %s', (session['start_station'],))
        station = cursor.fetchone()
        cursor.execute(
            'select * from metro WHERE line_id = %s', (station['line_id'],))
        metro = cursor.fetchone()
        # metro_id = metro['metro_id']
        # print("METRO ID =", metro_id)
        print("METRO ID =", station['line_id'])
        balance = metrocard_info['balance']
    # Check if "email_id", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'start' in request.form and 'dest' in request.form and 'gender' in request.form:
        # Create variables for easy access
        # fullname = request.form['fullname']
        start = request.form['start']
        dest = request.form['dest']
        gender = request.form['gender']

        cursor.execute('select max(user_id) from users')
        user_id = cursor.fetchone()
        print("user_id 1st =", user_id)

        cursor.execute('select max(ticket_id) from ticket')
        ticket_id = cursor.fetchone()
        print("ticket_id 1st =", ticket_id)

        cursor.execute(
            'select station_id from station WHERE station_name = %s', (start,))
        station_id = cursor.fetchone()
        print("station_id 1st =", station_id)

        now = datetime.now()
        now1 = dt.datetime.now()

        current_time = now.strftime("%H:%M:%S")
        print("Current Time =", current_time)

        if not start or not dest or not gender:
            flash('Please fill out the form!')
        elif start == dest:
            flash('Please fill out the form with correct station names!')
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

            st = ''.join(map(str, station_id))
            st1 = int(st)
            st1 = st1 + 1
            print("card_id 2nd =", station_id)
            station_id = st1

            num1 = int(start.split("_")[1])
            num2 = int(dest.split("_")[1])
            # fare = abs((num2-num1)*5)

            # start1 = int(start.split("_")[1])
            # dest1 = int(dest.split("_")[1])
            l1 = ["st_01", "st_02", "st_03", "st_04", "st_05", "st_06"]
            l2 = ["st_07", "st_08", "st_03", "st_09", "st_10", "st_11"]

            if(start in l1 and dest in l1):
                time_final = abs(num2 - num1)
                metro_id = 384951
            elif(start in l1 and dest in l2):
                start_index = l1.index(start)
                des_index = l2.index(dest)
                intersection1 = l1.index(list(set(l1) & set(l2))[0])
                intersection2 = l2.index(list(set(l1) & set(l2))[0])
                # print(intersection2)
                time_final = abs(des_index-intersection2) + \
                    abs(start_index-intersection1)
                # print(time_final)
                metro_id = 384951
            elif(start in l2 and dest in l1):
                start_index = l2.index(start)
                des_index = l1.index(dest)
                intersection1 = l1.index(list(set(l1) & set(l2))[0])
                intersection2 = l2.index(list(set(l1) & set(l2))[0])
                time_final = abs(des_index-intersection1) + \
                    abs(start_index-intersection2)
                metro_id = 384952
            else:
                start_index = l2.index(start)
                des_index = l2.index(dest)
                time_final = abs(des_index - start_index)
                metro_id = 384952
            print("\n\n\n ", time_final)
            fare = time_final*5

            today = datetime.today()
            print("Today's date:", today)
            today_date = today.strftime('%d:%m:%Y')
            current_time = dt.datetime.now()  # or dt.datetime.now(dt.timezone.utc)
            c_time = current_time.strftime('%H:%M:%S')
            dest_time = now + dt.timedelta(seconds=(time_final*600))
            d_time = dest_time.strftime('%H:%M:%S')
            print(c_time)
            print(d_time)
            print(dest_time)
            print(today_date)


# way
            st1_arr = [6, 5, 4, 3, 2, 1]
            st2_arr = [12, 11, 10, 9, 8, 7]
            time_line1 = [0, 5, 10, 15, 20, 25, 30, 35, 40,
                          45, 50, 55]  # 1 to 6 and 7 to 11 (-1)  5->25
            time_line2 = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55]
            if(start in l1):

                dest_time = now + dt.timedelta(seconds=(time_final*600))
                d_time = dest_time.strftime('%H:%M:%S')
                print(d_time)
                if((time_line1[num1-1]) >= now1.minute):
                    arr_t = time_line1[num1-1] - now1.minute
                else:
                    arr_t = time_line1[11-(num1-1)] - now1.minute
                # arr_t = (abs(num1-1))*5
                # arrival_time = ("%s:,%s:,%s", now1.hour, arr_t, now1.second)
                arrival_time = current_time + \
                    dt.timedelta(seconds=(arr_t*60))
                des_t = (abs(time_final))*5
                departure_time = arrival_time + \
                    dt.timedelta(seconds=(time_final*5*60))
                # waiting_time = arrival_time - current_time
            else:

                dest_time = now + dt.timedelta(seconds=(time_final*600))
                d_time = dest_time.strftime('%H:%M:%S')
                print(d_time)
                if((time_line1[num1-7]) >= now1.minute):
                    arr_t = time_line1[num1-7] - now1.minute
                else:
                    arr_t = time_line1[11-(num1-7)] - now1.minute
                # arr_t = (abs(num1-1))*5
                # arrival_time = ("%s:,%s:,%s", now1.hour, arr_t, now1.second)
                arrival_time = current_time + \
                    dt.timedelta(seconds=(arr_t*60))
                des_t = (abs(time_final))*5
                departure_time = arrival_time + \
                    dt.timedelta(seconds=(time_final*5*60))
                # waiting_time = dt.timedelta(
                #     arrival_time - current_time)

            print("final")
            waiting_time = arrival_time - current_time
            print(waiting_time)

            arrival_time = arrival_time.strftime('%H:%M')
            departure_time = departure_time.strftime('%H:%M')
            # waiting_time = waiting_time.strftime('%H:%M')

            print("\n arrival_time =", arrival_time)
            print("\n departure_time = ", departure_time)
            # print("\n waiting_time = ", waiting_time)

            # arrival_time =
            # print("point_id =", point_id)

            cursor.execute("INSERT INTO users (user_id, gender, station_id) VALUES (%s,%s,%s)",
                           (user_id, gender, station_id,))
            cursor.execute("INSERT INTO ticket (ticket_id, date_cur , start_time, end_time, fare, start, destination, user_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
                           (ticket_id, today_date, c_time, departure_time, fare, start, dest, user_id,))
            cursor.execute("INSERT INTO platform (platform_no,arrival_time, departure_time, waiting_time, station_id, user_id) VALUES (%s,%s,%s,%s,%s,%s)",
                           (1, arrival_time, departure_time, waiting_time, station_id, user_id,))
            cursor.execute("INSERT INTO boards (metro_id, user_id, station_id) VALUES (%s,%s,%s)",
                           (metro_id, user_id, station_id,))

            # cursor.execute("INSERT INTO users (email_id, fullname, password, passwordopen, p_no, card_id) VALUES (%s,%s,%s,%s,%d,%d)",
            #                (email_id, fullname, _hashed_password, passwordopen, p_no, card_id))

            # cursor.execute('UPDATE metro_card SET balance = (%s) WHERE email_id= %s',
            #                (session['email_id'], balance-fare,))
            cursor.execute('UPDATE metro_card SET (balance ,start ,destination ,s_time ,d_time) = (%s,%s,%s,%s,%s) WHERE email_id= %s',
                           (balance-fare, start,
                            dest, arrival_time, departure_time, session['email_id'],))

            # cursor.execute("INSERT INTO users (email_id, fullname, password, passwordopen, p_no, card_id) VALUES (%s,%s,%s,%s,%d,%d)",
            #                (email_id, fullname, _hashed_password, passwordopen, p_no, card_id))

            conn.commit()
            cursor.execute(
                'select * from station WHERE station_name = %s', (start,))
            station = cursor.fetchone()

            cursor.execute(
                'select * from boards WHERE user_id = %s', (user_id,))
            boards = cursor.fetchone()

            cursor.execute(
                'select * from platform WHERE user_id = %s', (user_id,))
            platform = cursor.fetchone()

            print("platform       1st =", platform)
            cursor.execute('select * from metro_card WHERE email_id= %s',
                           (session['email_id'],))
            metro_card = cursor.fetchone()

            conn.commit()
            # wait_t = metro_card['s_time'] - c_time
            # print("WAIT TIME = ", wait_t)
            flash('You have successfully booked!')
            return render_template('bookings.html', metro_id=metro_id, metro=metro, metro_card=metro_card, station=station, boards=boards, gender=gender, waiting_time=waiting_time,)
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        flash('outer Please fill out the form!')
    # Show registration form with message (if any)
    return render_template('bookings.html', metro_card=metro_card, station=station, metro=metro, waiting_time=waiting_time, )


if __name__ == "__main__":
    app.run(debug=True)
