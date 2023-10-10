# Contact-List
This project contains a web contact list mainly relying on the following Python modules: Flask and Sqlalchemy.
The homepage displays the wohle list contacts with the posibility to sort them alphabatically based on specific tags.
The user has the option to edit/delete a contact or add new ones.
All contacts are stored within a Data Base File.

There is also a "reminder.py" file which has to be run independently (preferably on a daily basis). 
This file simply checks all of the contacts' dates of birth and sends you an email notification if it is their birthday.
