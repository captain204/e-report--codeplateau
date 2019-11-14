from flask import Flask, render_template, request, redirect, flash, url_for, session, logging
from data import newsArticles
# from flask import newsArticles
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
# from login_manager import LoginManager

app = Flask(__name__)


@app.route ("/")
@app.route ("/index")
def homepage():
    return render_template("index.html", title= "homepage")
    


app.config['SECRET_KEY'] = 'your_secret_string'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'diane'
app.config['MYSQL_PASSWORD'] = '123Spirit##'
app.config['MYSQL_DB'] = 'blackbook'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

class RegisterForm(Form):
    name = StringField(u'Name', validators=[validators.input_required(), validators.Length(min=3, max=50)])
    email = StringField(u'Email', validators=[validators.input_required(), validators.Length(min=3, max=50)])
    username = StringField(u'Username', validators=[validators.input_required(), validators.Length(min=3, max=50)])
    password = PasswordField('Password', [validators.DataRequired(), validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')

@app.route('/register', methods=['GET', 'POST'])
def users():
    form = RegisterForm(request.form)
    if request.method =='POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))


        #create cursor
        cur = mysql.connection.cursor()

        # validating username
        user = cur.execute("select * from USERS where username = %s", [username])
        if user > 0:
            flash("username already taken", "danger")
            return render_template("register.html", form=form)

        # validating emails
        email_con = cur.execute("select * from USERS where email = %s", [email])

        if email_con > 0:
            flash("email taken by another user", "danger")
            return render_template("register.html", form=form)


        else:

            cur.execute("INSERT INTO USERS (name, email, username, password) VALUES (%s, %s, %s, %s)", (name, email, username, password))

        # commit to db
            mysql.connection.commit()




        # close connection
            cur.close()
        # flash message
            flash('you are welcome to the club', 'success')
            return redirect(url_for("login"))
        # return render_template('/register.html')
    return render_template('/register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method =='POST':
    # get form fields
        username = request.form['username']
        password_candidate = request.form['password']


        # create cursor
        cur = mysql.connection.cursor()
        
        # get user by user name
        result = cur.execute("SELECT * FROM USERS WHERE username = %s", [username])
    
        if result > 0:
            # getting the hash
            data = cur.fetchone()
            password = data['password']
            
            # comparing passwwords
            if sha256_crypt.verify(password_candidate, password):
                app.logger.info('password matched')
                session['logged_in'] = True
                session['username'] = username

                flash('you are successfully logged in', 'success')
                return redirect(url_for('dashboard'))
            else:
                # app.logger.info('password mismatch')  
                error ='Invalid login details'
                return render_template('login.html',error=error)  
                

        else:
            # app.logger.info('user not found')
            error = 'User not found'
            return render_template('login.html',error=error)  

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('/dashboard.html')


if __name__ == '__main__':

    app.secret_key='secret1234'

    app.run(debug = True)