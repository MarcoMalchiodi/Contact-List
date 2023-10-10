from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect
from datetime import date
import smtplib

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contact-database.db'
db = SQLAlchemy(app)
app.app_context().push()


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    surname = db.Column(db.String, nullable=False)
    birthday = db.Column(db.String, nullable=False)
    nationality = db.Column(db.String, nullable=False)
    industry = db.Column(db.String, nullable=False)
    custom_tag1 = db.Column(db.String, nullable=False)
    custom_tag2 = db.Column(db.String, nullable=False)
    custom_tag3 = db.Column(db.String, nullable=False)

    
if not inspect(db.engine).has_table('contact'):
    db.create_all()
    

all_contacts = db.session.query(Contact).all() # the date is YYYY-MM-DD format (string)

today = str(date.today()) # YYYY-MM-DD format


# ----------- NOTIFICATION SENDER -------------- #

my_email = "randomemailaddr@gmail.com"
my_password = "password_goes_here"

for contact in all_contacts:
    if contact.birthday[-5:] == today[-5:]:
        with smtplib.SMTP('smtp.gmail.com') as connection:
                connection.starttls()
                connection.login(user=my_email, password=my_password)
                connection.sendmail(from_addr=my_email, to_addrs=my_email,msg=f"Subject: Birthday Notification \n\nIt's {contact.name} {contact.surname}'s birthday today!")