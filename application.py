from flask import(Flask,render_template,redirect,request,flash,url_for,session,logging)
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt
from wtforms import Form, StringField, TextAreaField,PasswordField,SelectField,FileField, validators
from functools import wraps
import os
import re
import time


app = Flask(__name__)

mysql = MySQL(app)

app.config['SECRET_KEY'] = 'fjfjkfkjssmdjdjdmdm'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Olu1989!@'
app.config['MYSQL_DB'] = 'eReport'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# app.config['SECRET_KEY'] = 'fjfjkfkjssmdjdjdmdm'
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = ''
# app.config['MYSQL_DB'] = 'quiz'
# app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# app = Flask(__name__)

# mysql = MySQL(app)

# app.config['SECRET_KEY'] = 'fjfjkfkjssmdjdjdmdm'
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = ''
# app.config['MYSQL_DB'] = 'e-report'
# app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

#DATETIME VARIABLE FOR 'UPDATE AT' COLUMN IN MYSQL
now = time.strftime('%Y-%m-%d %H:%M:%S')


# ********************************************************************************
# *************************CLASS & FUNCTION***************************************
"""" ALL Form validation Should go here """
class Comment(Form):
    subject= StringField(u'Subject',validators=[validators.input_required(),
    validators.Length(min=10,max=250)])
    body = TextAreaField(u'Body', validators=[validators.input_required(),validators.Length(max=2000)])


#EMPLOYEE REPORT FORM CLASS
class ReportForm(Form):
    title = StringField(u'Title', validators=[validators.input_required(), validators.length(min=3,max=200)])
    body = TextAreaField(u'Body', validators=[validators.input_required(), validators.length(min=10)])
    file = FileField(u'File')


#CHECK IF USER IS LOGGED IN
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login','danger')
            return redirect(url_for("login"))
    return wrap


# ********************************************************************************
# ****************************REGISTER, LOGIN & DASHBOARD SELECTOR****************
""" All Web Routes """
@app.route('/', methods=['GET','POST'])
def index():
    pass


#REGISTER
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        email = request.form['email']
        password = sha256_crypt.encrypt(str(request.form['password']))
        is_admin = request.form['is_admin']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        image = request.form['image']
        department = request.form['department']
        position = request.form['position']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE username = %s', [username])
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO users (username,email, password, is_admin,firstname, lastname, image, department, position) VALUES (%s, %s, %s,%s, %s, %s,%s, %s, %s)', (username,email, password, is_admin,firstname, lastname, image, department, position))
            mysql.connection.commit()
            #close the cursor
            cursor.close()

            flash('You Are Successfully Registered!')
            return render_template('login.html')

    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
        return render_template('register.html', msg=msg)
    else:
    # Show registration form with message (if any)
        return render_template('register.html')


#LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password_candidate = request.form['password']

        # Check if account exists using MySQL
        cursor = mysql.connection.cursor()
        result = cursor.execute('SELECT * FROM users WHERE username = %s', [username])
        
        if result>0:
            # Fetch one record and return result
            account = cursor.fetchone()

            password = account['password']

            #compare passwords
            if sha256_crypt.verify(password_candidate, password):
            # If account exists in accounts table in out database
                # Create session data, we can access this data in other routes
                session['logged_in'] = True
                # session['id'] = account['id']
                session['username'] = account['username']
                # Redirect to dashboard
                return redirect(url_for('select_dashboard'))
            else:
                # Account doesnt exist or username/password incorrect
                msg = 'Incorrect username/password!'
                return render_template('login.html', msg=msg)
        else:
            msg = 'Incorrect username/password!'
            return render_template('login.html', msg=msg)
    return render_template('login.html', msg='')


#THIS ROUTE DECIDES WHICH DASHBOARD IS RENDERED (ADMIN OR EMPLOYEE)
@app.route('/select/dashboard')
@is_logged_in
def select_dashboard():
    # session['username'] = 'emeka'
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE username = %s", [session['username']])
    user_dashboard = cur.fetchone()
    if user_dashboard['is_admin'] == '0':
        session['user'] = user_dashboard #'user' in employeenavbar get fed with this
        session['id'] = user_dashboard['id']
        cur.execute("SELECT * FROM report WHERE user_id = %s", [user_dashboard['id']])
        report = cur.fetchall()
        lens = len(report)
        return render_template('employee/dashboard.html', user=session['user'], reports=report, lens=lens, dashboard='active', page='Dashboard')
    else:
        return redirect(url_for('dashboard')) #redirect to Admin dashboard


# ********************************************************************************
# *********************************EMPLOYEE PAGES*********************************
#ADD REPORT
@app.route('/employee/add_report', methods=["GET","POST"])
@is_logged_in
def add_employee_report():
    form = ReportForm(request.form)
    if request.method == "POST" and form.validate():
        #get form fields
        title = form.title.data
        description = form.body.data
        file = form.file.data
        
        #create cursor
        cur = mysql.connection.cursor()

        #post data into database
        cur.execute ("INSERT INTO report (title, description, file, user_id) VALUES (%s, %s, %s, %s)", (title, description, file, session['id']))

        # commit to database
        mysql.connection.commit()

        #close the cursor
        cur.close()

        #flash a message
        flash("Report successfully added!", "success") #success is a category
        return render_template("employee/add_report.html", form=form,  user=session['user'], add_report='active', page='Add Report')
    #if request.method == "GET"
    return render_template("employee/add_report.html", form=form,  user=session['user'], add_report='active', page='Add Report')


#VIEW REPORT
@app.route('/employee/view_report')
@is_logged_in
def view_employee_report():
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM report WHERE user_id = %s", [session['user']['id']])
    report = cur.fetchall()
    if result >0:
        return render_template('employee/view_report.html', user=session['user'], reports=report, view_report='active', page='View Report')
    else:
        msg = 'No Report Found'
        return render_template("employee/view_report.html", user=session['user'], msg=msg)
    #Close cursor
    cur.close()


#LOGOUT
@app.route("/logout")
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for("login"))
    

#UPDATE/EDIT REPORT
@app.route("/employee/update_report/<string:id>/", methods=["GET","POST"])
@is_logged_in
def update_employee_report(id):
    #if request.method == "GET"

    #create cursor
    cur = mysql.connection.cursor()
    #Fetch single row with the article's id
    cur.execute("SELECT * FROM report WHERE id = %s", [id]) 
    
    report = cur.fetchone()   #select single report with the id from table
    
    #Get form
    form = ReportForm(request.form)
    
    #Populate the Article form field
    form.title.data = report['title']
    form.body.data = report['description']
    form.file.data = report['file']

    if request.method == "POST" and form.validate():
        #get form fields
        title = request.form['title']
        description = request.form['body']
        file = request.form['file']
    
        #create cursor
        cur = mysql.connection.cursor()

        #post data into database
        cur.execute ("UPDATE report SET title=%s, description=%s, file=%s, updated_at=%s WHERE id=%s", (title, description, file, now, id))

        # commit to database
        mysql.connection.commit()

        #close the cursor
        cur.close()

        #flash a message
        flash("Report Updated successfully!", "success") #success is a category
        return redirect(url_for("view_employee_report"))
    return render_template("employee/update_report.html", form=form, id=id, user=session['user'], view_report='active', page='Update Report')


#DELETE REPORT
@app.route("/employee/delete_report/<string:id>/", methods=["POST"])
@is_logged_in
def delete_employee_report(id):

    #create cursor
    cur = mysql.connection.cursor()

    #Delete single row with the report's id
    cur.execute ("DELETE FROM report WHERE id=%s", [id])
    
    # commit to database
    mysql.connection.commit()

    #close the cursor
    cur.close()

    #flash a message
    flash("Report Deleted Successfully!", "success") #success is a category
    return redirect(url_for("view_employee_report"))


# ********************************************************************************
# *****************************************ADMIN PAGES****************************
@app.route('/dashboard', methods=['GET','POST'])
#@is_logged_in
def dashboard():
    cur = mysql.connection.cursor()
    cur.execute("SELECT users.id, users.firstname, users.lastname, report.title, report.description, report.file FROM users INNER JOIN report ON users.id = report.user_id ORDER BY users.id DESC")
    reports = cur.fetchall()
 
    cur = mysql.connection.cursor()
    cur.execute("SELECT COUNT(*) FROM report")
    report_count = cur.fetchall()

    return render_template('admin/dashboard.html', reports = reports, report_count = report_count)

@app.route('/staffs', methods=['GET','POST'])
def staffs():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    return render_template('admin/users.html',users = users)

@app.route("/staffs_delete/<string:id>/",methods=['POST'])
def staffs_delete(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM users WHERE id =%s", [id])
    mysql.connection.commit()
    cur.close()
    flash("Delete Completed","danger")
    return redirect(url_for('staffs'))

@app.route("/message",methods=['GET'])
def message():
    user_id = 1 #Session will be set to pass user_id during login
    cur = mysql.connection.cursor()
    cur.execute("SELECT users.id, users.image, comment.user_id, comment.title, comment.subject, comment.body, comment.admin FROM users INNER JOIN comment ON users.id = comment.user_id WHERE users.id=%s",[user_id])
    messages = cur.fetchall()
    return render_template("employee/dashboard.html", messages = messages)

@app.route("/message_view/<string:id>", methods=['GET'])


@app.route("/comment/<string:id>", methods=['GET','POST'])
def comment(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * from users WHERE id=%s",[id])
    user = cur.fetchone()
    cur = mysql.connection.cursor()
    cur.execute("SELECT * from report WHERE user_id=%s",[id])
    report = cur.fetchone()
    #Mapping a user to a specific report
    user_id = user['id']
    username = user['username']
    title = report['title']
    # Insert into comments table
    form = Comment(request.form) 
    if request.method == 'POST' and form.validate():
        subject = form.subject.data
        body = form.body.data
        admin = "random" #Admin username will be placed here
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO comment (user_id, username, title, subject, body, admin) VALUES(%s, %s, %s, %s, %s, %s)",(user_id, username, title, subject, body, admin))
        mysql.connection.commit()
        cur.close()
        flash('Messaage sent successfuly','success')
        return redirect(url_for('dashboard'))
    
    return render_template("admin/message.html",  form=form)


if  __name__ == "__main__":
    app.run(debug=True)
