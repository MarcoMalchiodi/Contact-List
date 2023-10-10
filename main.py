from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect

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

    def __getitem__(self, key):
        # Define a custom method to access attributes using dictionary-style notation
        # For example, contact['name']
        if hasattr(self, key):
            return getattr(self, key)
        else:
            raise KeyError(f"'{key}' not found in Contact")
        
    
if not inspect(db.engine).has_table('contact'):
    db.create_all()
    
id_counter = db.session.query(Contact).count()


'''new_contact = Contact(
    name = "Vincenzo",
    surname = "Agostini",
    birthday = "10/09/1900",
    nationality = "Italy",
    industry = "Farmer",
    custom_tag1 = "",
    custom_tag2 = "",
    custom_tag3 = "",
)
db.session.add(new_contact)
db.session.commit()'''
   


# ------------ HTML INTERACTION  --------------- #

@app.route("/")
def home():
    # deleting duplicates due to a bug caused by session.commit()
    all_contacts = db.session.query(Contact).all()
    for x in range(1, len(all_contacts)):
        if all_contacts[x-1].name == all_contacts[x].name and all_contacts[x-1].surname == all_contacts[x].surname and all_contacts[x-1].birthday == all_contacts[x].birthday:
            contact_to_delete = Contact.query.get(all_contacts[x].id)
            db.session.delete(contact_to_delete)
            db.session.commit()
        all_contacts = db.session.query(Contact).all()
        
    return render_template("index.html", contacts=all_contacts)

@app.route("/delete",methods=['GET','POST'])
def delete():
    id_to_delete= int(request.args.get('contact_id'))
    all_contacts = db.session.query(Contact).all()
    for contact in all_contacts:
        if id_to_delete == contact.id:
            contact_to_delte = contact
            db.session.delete(contact_to_delte)
            db.session.commit()
    return redirect(url_for('home'))

@app.route("/edit", methods=['GET','POST'])
def edit():
    if request.method == 'POST':
        all_contacts = db.session.query(Contact).all()
        contact_id = int(request.args.get('contact_id'))
        for contact in all_contacts:
            if contact_id == contact.id:
                contact_to_edit = contact
        contact_to_edit.name = request.form['name']
        contact_to_edit.surname = request.form['surname']
        contact_to_edit.birthday = str(request.form['birthdate'])
        contact_to_edit.industry = request.form['industry']
        contact_to_edit.custom_tag1 = request.form['custom-tag1']
        contact_to_edit.custom_tag2 = request.form['custom-tag2']
        contact_to_edit.custom_tag3 = request.form['custom-tag3']
        db.session.commit()
        return redirect(url_for('home'))
    
    
    id_to_edit = int(request.args.get('contact_id'))
    all_contacts = db.session.query(Contact).all()
    for contact in all_contacts:
        if id_to_edit == contact.id:
            contact_to_edit = contact
    return render_template("edit.html",contact=contact_to_edit)
        

@app.route("/add",methods=['GET','POST'])
def add():
    if request.method == 'POST':
        new_name = request.form['name']
        new_surname = request.form['surname']
        new_birthday = str(request.form['birthdate'])
        new_nationality = request.form['nationality']
        new_industry = request.form['industry']
        new_custom_tag1 = request.form['custom-tag1']
        new_custom_tag2 = request.form['custom-tag2']
        new_custom_tag3 = request.form['custom-tag3']
        
        new_contact = Contact(
            name = new_name,
            surname = new_surname,
            birthday = new_birthday,
            nationality = new_nationality,
            industry = new_industry,
            custom_tag1 = new_custom_tag1,
            custom_tag2 = new_custom_tag2,
            custom_tag3 = new_custom_tag3,
        )
        db.session.add(new_contact)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("add_contact.html")


def sort_contacts(contact_list, tag):
    unordered_list = []
    
    if tag == "name":
        for contact in contact_list:
            unordered_list.append(contact.name)
    elif tag == "surname":
        for contact in contact_list:
            unordered_list.append(contact.surname)
    elif tag == "industry":
        for contact in contact_list:
            unordered_list.append(contact.industry)
    elif tag == "birthday":
        for contact in contact_list:
            unordered_list.append(str(contact.birthday))
    elif tag == "nationality":
        for contact in contact_list:
            unordered_list.append(contact.surname)
    
    sorted_list = sorted(unordered_list)
    return sorted_list


################### TO FIX #################
@app.route("/sorted_cont",methods=['GET','POST'])
def sorted_cont():
    if request.method=="POST":
        tag = request.form['selectOption']
        all_contacts = db.session.query(Contact).all()
        sorted_list = sort_contacts(all_contacts,tag)
        sorted_contacts = []
        
        for x in sorted_list:
            for contact in all_contacts:
                if contact[tag] == x:
                    sorted_contacts.append(contact)
        
        contacts_to_delete = []

        for x in range(1, len(sorted_contacts)):
            if sorted_contacts[x-1].name == sorted_contacts[x].name and sorted_contacts[x-1].surname == sorted_contacts[x].surname and sorted_contacts[x-1].birthday == sorted_contacts[x].birthday:
                contacts_to_delete.append(sorted_contacts[x])

        # Delete the contacts outside of the loop
        for contact_to_delete in contacts_to_delete:
            db.session.delete(contact_to_delete)
            
        db.session.commit()
            

        return render_template("sorted.html",sorted_contacts=sorted_contacts)
    return redirect(url_for('home'))



if __name__ == '__main__':
    app.run(debug=True)

        
