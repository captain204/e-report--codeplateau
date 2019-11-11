from flask import(Flask,Blueprint,render_template,redirect,request,flash,url_for,session,logging)
from flask_mysqldb import MySQL
import os
from flask_wtf import FlaskForm
from flask import current_app as app
# from src.models.products.product import Product
from passlib.hash import sha256_crypt
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, SelectField,SubmitField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from flask_uploads import UploadSet, IMAGES
from functools import wraps
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = ''
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)

mysql = MySQL(app)

app.config['SECRET_KEY'] = 'fjfjkfkjssmdjdjdmdm'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'codepl'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    
if  __name__ == "__main__":
    app.run(debug=True)
