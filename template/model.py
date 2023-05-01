'''
    Our Model class
    This should control the actual "logic" of your website
    And nicely abstracts away the program logic from your page loading
    It should exist as a separate layer to any database or data structure that you might be using
    Nothing here should be stateful, if it's stateful let the database handle it
'''
# from sql import SQLDatabase
import view
import random
import hashlib
import os
# from sqlite3 import DatabaseError
from no_sql_db import Table
from no_sql_db import DATABASE
# Initialise our views, all arguments are defaults for the template
page_view = view.View()
# DATABASE = SQLDatabase()
# SQLDatabase.database_setup()
# DATABASE = DB()
# USERS = Table()
# USERS.create_entry(0, "admin", "ghdjdh7388298#+sj", 1)
# DATABASE.add_table("users", "id", "username", "password", "admin")
USERS = DATABASE.get_table("users")
#-----------------------------------------------------------------------------
# Index
#-----------------------------------------------------------------------------

def index():
    '''
        index
        Returns the view for the index
    '''
    return page_view("index")

#-----------------------------------------------------------------------------

# Register
#-----------------------------------------------------------------------------

def register_form():
    '''
        register_form
        Returns the view for the register_form
    '''
    return page_view("register")


# -----------------------------------------------------------------------------

# Check the register credentials
def register_check(username, password):
    '''
        register_check
        Checks usernames and passwords

        :: username :: The username
        :: password :: The password

        Returns either a view for valid credentials, or a view for invalid credentials
    '''

    # By default assume good creds
    register = True
    admin = False

    user_taken = DATABASE.search_table("users", "username", username)

    if user_taken != None:
        err_str = "Username taken!"
        register = False

    if username == "":  # Invalid Username
        err_str = "Please enter a username"
        register = False

    if password == "":  # Invalid password
        err_str = "Please enter a password"
        register = False

    if len(password) < 14:
        err_str = "Please enter a stronger password"
        register = False

    has_special_char = False
    for k in password:
        if k in "!@#$%^&*+=-":
            has_special_char = True
            break

    if has_special_char == False:
        err_str = "Password must contain at least one special character"
        register = False

    has_digit = False
    for k in password:
        if k.isdigit():
            has_digit = True
            break

    if has_digit == False:
        err_str = "Password must contain at least one number"
        register = False

    if register:
        salt = os.urandom(32)
        pw = str(password).encode('utf-8')
        salted_pw = salt+pw
        secure_password = hashlib.sha256(salted_pw).hexdigest()
        id = len(USERS.entries)
        DATABASE.create_table_entry("users", id, username, salt, secure_password, 0)
        return page_view("valid_register", name=username)
    else:
        return page_view("invalid", reason=err_str)

#-----------------------------------------------------------------------------
# Login
#-----------------------------------------------------------------------------

def login_form():
    '''
        login_form
        Returns the view for the login_form
    '''
    return page_view("login")

#-----------------------------------------------------------------------------

# Check the login credentials
def login_check(username, password):
    '''
        login_check
        Checks usernames and passwords

        :: username :: The username
        :: password :: The password

        Returns either a view for valid credentials, or a view for invalid credentials
    '''

    # By default assume good creds
    login = True

    user = DATABASE.search_table("users", "username", username)

    if user == None: # user does not exist
        err_str = "Incorrect Username"
        login = False

    else:
        stored_pass = DATABASE.search_2_values("users", "username", username, "password")
        stored_salt = DATABASE.search_2_values("users", "username", username, "salt")
        pw = str(password).encode('utf-8')
        salted_pw = stored_salt + pw
        hashed_pass = hashlib.sha256(salted_pw).hexdigest()
        if stored_pass != hashed_pass: # Wrong password
            err_str = "Incorrect Password"
            print(f"stored: {stored_pass}, given: {hashed_pass}")
            login = False
        
    if login: 
        return page_view("valid", name=username)
    else:
        return page_view("invalid", reason=err_str)

#-----------------------------------------------------------------------------
# About
#-----------------------------------------------------------------------------

def about():
    '''
        about
        Returns the view for the about page
    '''
    return page_view("about", garble=about_garble())



# Returns a random string each time
def about_garble():
    '''
        about_garble
        Returns one of several strings for the about page
    '''
    garble = ["leverage agile frameworks to provide a robust synopsis for high level overviews.", 
    "iterate approaches to corporate strategy and foster collaborative thinking to further the overall value proposition.",
    "organically grow the holistic world view of disruptive innovation via workplace change management and empowerment.",
    "bring to the table win-win survival strategies to ensure proactive and progressive competitive domination.",
    "ensure the end of the day advancement, a new normal that has evolved from epistemic management approaches and is on the runway towards a streamlined cloud solution.",
    "provide user generated content in real-time will have multiple touchpoints for offshoring."]
    return garble[random.randint(0, len(garble) - 1)]


#-----------------------------------------------------------------------------
# Debug
#-----------------------------------------------------------------------------

def debug(cmd):
    try:
        return str(eval(cmd))
    except:
        pass


#-----------------------------------------------------------------------------
# 404
# Custom 404 error page
#-----------------------------------------------------------------------------

def handle_errors(error):
    error_type = error.status_line
    error_msg = error.body
    return page_view("error", error_type=error_type, error_msg=error_msg)