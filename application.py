from flask import(Flask,render_template,redirect,request,flash,url_for,session,logging)
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt
from wtforms import Form, StringField, TextAreaField,PasswordField,SelectField, validators
from functools import wraps

app = Flask(__name__)

mysql = MySQL(app)

app.config['SECRET_KEY'] = 'fjfjkfkjssmdjdjdmdm'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'e-report'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'


"""" ALL Form validation Should go here """
class Comment(Form):
    subject= StringField(u'Subject',validators=[validators.input_required(),
    validators.Length(min=10,max=250)])
    body = TextAreaField(u'Body', validators=[validators.input_required(),validators.Length(max=2000)])


""" All Web Routes """
@app.route('/', methods=['GET','POST'])
def index():
    pass




@app.route('/dashboard', methods=['GET','POST'])
#@is_logged_in
def dashboard():
    cur = mysql.connection.cursor()
    cur.execute("SELECT users.id, users.firstname, users.lastname, report.title, report.description, report.file FROM users INNER JOIN report ON users.id = report.user_id ORDER BY users.id DESC")
    reports = cur.fetchall()
 
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM report")
    cur.fetchall()
    report_count = cur.rowcount()

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
    cur.execute("SELECT users.id, users.image, comment.user_id, comment.title, comment.subject, comment.body, comment.admin FROM users INNER JOIN comment ON users.id = comment.user_id WHERE comment.user_id=%s",[user_id])
    messages = cur.fetchall()
    return render_template("employee/dashboard.html", messages = messages)

@app.route("/message_view/<string:id>", methods=['GET'])
def message_view(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM comment WHERE id=%s",[id])
    message = cur.fetchone()
    return render_template("employee/message_view.html", message = message)


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
