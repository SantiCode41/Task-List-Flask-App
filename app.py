from flask import Flask, redirect, render_template, request, session, send_file
from flask_session import Session
from cs50 import SQL
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required, error_handling  # excel_generator
import datetime
# import os

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Sets up the connection to the classlist database
db = SQL("sqlite:///classlist.db")

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Main page accessible only after log in
@app.route("/")
@login_required
def index():
    return render_template("index.html", active_page="Dashboard")


# Landing page to show preview of site as well as links to log in and sign in
@app.route("/landingpage")
def landingPage():
    return render_template("landingpage.html", active_page="Log In")


# Log in process
@app.route("/login", methods=["GET", "POST"])
def login():

    session.clear()

    if request.method == "POST":
        if not request.form.get("username"):  # Checks if username was entered
            return error_handling("Must provide a username", 400)

        elif not request.form.get("password"):  # Checks if password was entered
            return error_handling("Must provide a password", 400)

        userInfo = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))  # Queries DB for the account information provided

        if len(userInfo) != 1 or not check_password_hash(userInfo[0]["password_hash"], request.form.get("password")):  # returns error if no such account is found
            return error_handling("User not found and/or password was incorrect", 400)

        session["user_id"] = userInfo[0]["user_id"]  # Estabishes current user

        return redirect("/")  # Redirects user to dashboard

    #  If method is GET user is redirected to the login page
    else:
        return render_template("login.html", active_page="Log In")


# Log OUT process
@app.route("/logout")
@login_required
def logout():
    """Logs user out"""

    session.clear()  # Clears user infor such as user_id

    return redirect("/login")  # Returns user to the login screen after having logged out


# Sign up/registration of new user process
@app.route("/signup", methods=["GET", "POST"])
def signUp():

    session.clear()  # Clears user infor such as user_id

    if request.method == "POST":
        # Gets information from form
        username = request.form.get("username")
        password = request.form.get("password")
        password_confirmation = request.form.get("password_confirmation")

        users = db.execute("SELECT * FROM users")  # Gets list of current users

        if not username:
            return error_handling("Must provide a username", 400)  # Checks if a username was provided
        for user in users:
            if user.get('username') == username:
                return error_handling("Username provided is not available", 400)  # Checks if username provided is already taken by another user
        if not password:  # MAYBE swap this line with "for user in users" to prevent checking all username to see if username is taken if no password was provided (might reduce server usage)
            return error_handling("Must provide a password", 400)  # Checks if password was provided
        elif not password_confirmation:
            return error_handling("must re-enter password", 400)  # Checks if password confirmation was provided

        if password != password_confirmation:
            return error_handling("Passwords must match", 400)  # Checks if password and confirmation match

        password_hash = generate_password_hash(password)  # Generates password_hash to store in DB
        timestamp = datetime.datetime.now() # Timestamp of account's creation
        userLists = username + "_lists" # Generates table name for table to store new user's list items

        # # Makes folder for new user to temp hold generated excel files
        # folderName = username + "_temp_excel_files"
        # folderPath =

        # fullPath = os.path.join(folderPath, folderName)
        # os.makedirs(fullPath)

        # Adds new user to  DB/users
        db.execute("INSERT INTO users (username, password_hash, datetime_added) VALUES (?, ?, ?)", username, password_hash, timestamp)

        # Creates a new table that will store all of the new user's lists
        db.execute("CREATE TABLE IF NOT EXISTS ? (user_id INTEGER, list_id INTEGER PRIMARY KEY, list_table_name TEXT, list_title TEXT, FOREIGN KEY (user_id) REFERENCES users(user_id))", userLists)

        return redirect("/login")  # Sends user back to log in page so that they can log in with their new accout informaiton

    # If method = GET provide user with signup page
    else:
        return render_template("signup.html", active_page="Sign Up")


# Page navigation implementation
# MAYBE - Replace with JavaScript???
@app.route("/myaccount")
@login_required
def myaccount():

    # Get all of user's info to render to the "My Account" page
    userInfo = db.execute("SELECT user_id, username, datetime_added FROM users WHERE user_id = ?", session["user_id"])
    if len(userInfo) != 1:
        return error_handling("Invalid user count returned", 400)

    # format time stamp before sending to page
    timestampString = userInfo[0]["datetime_added"]
    timestamp = datetime.datetime.strptime(timestampString, "%Y-%m-%d %H:%M:%S")
    timestampFormated = timestamp.strftime("%B %d, %Y")

    return render_template("myaccount.html", userInfo=userInfo, dateInfo=timestampFormated, active_page="My Account")


# Change Password
@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    if request.method == "POST":
        userPasswordHash = db.execute("SELECT password_hash FROM users WHERE user_id = ?", session["user_id"])
        userPasswordHash = userPasswordHash[0]["password_hash"]

        if not check_password_hash(userPasswordHash, request.form.get("current_password")):
            return error_handling("Incorrect current password", 400)

        newPassword = request.form.get("new_password")
        newPasswordConfirmation = request.form.get("new_password_confirmation")
        if newPassword != newPasswordConfirmation:
            return error_handling("New password inputs did not match", 400)

        newPasswordHash = generate_password_hash(newPassword)
        db.execute("UPDATE users SET password_hash = ? WHERE user_id = ?", newPasswordHash, session["user_id"])

        return redirect("/myaccount")

    else:
        return render_template("changepassword.html", active_page="My Account")


# ACCOUNT DELETION
@app.route("/delete_account", methods=["GET", "POST"])
@login_required
def delete_account():
    if request.method == "POST":  # CORRECT - This only checks if passwords match not if password is correct!!!!!!
        if request.form.get("password") != request.form.get("password_confirmation"):
            return error_handling("Password inputs did not match", 400)

        userInfo = db.execute("SELECT * FROM users WHERE user_id = ?", session["user_id"])  # Queries DB for the account information provided

        if not check_password_hash(userInfo[0]["password_hash"], request.form.get("password")):  # returns error if passwords do not match
            return error_handling("Password is incorrect", 400)

        else:
            userInfo = db.execute("SELECT * FROM users WHERE user_id = ?", session["user_id"])
            username = userInfo[0]["username"]

            userListsTable = username + "_lists"

            listTableNamesData = db.execute("SELECT list_table_name FROM ?", userListsTable)
            listTableNames = []
            for item in listTableNamesData:
                listTableNames.append(item["list_table_name"])
            print(f"\n\nPrinting Here\n{listTableNames}\n\n\n")

            for table in listTableNames:
                db.execute("DROP TABLE ?", table)

            db.execute("DROP TABLE ?", userListsTable)

            db.execute("DELETE FROM users WHERE user_id = ?", session["user_id"])

            return render_template("/deletionconfirmation.html")
    else:
        return render_template("deleteaccount.html", active_page="My Account")


@app.route("/about")
def about():
    return render_template("about.html", active_page="About")


@app.route("/view_lists")
@login_required
def viewlists():

    # Gets the currect user's username - This is needed to generate names for new lists the user creates
    username = db.execute("SELECT username FROM users WHERE user_id = ?", session["user_id"])
    username = username[0]["username"]  # Extracts the username string from the returned list fo dicts
    table = username + "_lists"
    listsOfUser = db.execute("SELECT * FROM ?", table)  # Get all the lists this user has made

    # namesOfListsOfUser = []
    # for i in range(len(listsOfUser)):
    #     namesOfListsOfUser.append(listsOfUser[i]["list_name"])

    return render_template("viewlists.html", username=username, listInfo=listsOfUser, active_page="Dashboard")


# @app.route("/userguide")
# @login_required
# def userguide():
#     return render_template("userguide.html")


# @app.route("/support")
# @login_required
# def support():
#     return render_template("support.html")


# List generator
@app.route("/new_list", methods=["GET", "POST"])
@login_required
def list_generator():
    if request.method == "POST":
        tasklist = request.form.get("tasklist")  # Gets list in raw text form as entered by the user
        title = request.form.get("listname")  # Gets title (aka name) of the new list

        # Gets the currect user's username - This is needed to generate names for new lists the user creates
        username = db.execute("SELECT username FROM users WHERE user_id = ?", session["user_id"])
        username = username[0]["username"]  # Extracts the username string from the returned list fo dicts

        tasklist = tasklist.split(",")  # Generates a list of tasks provided by the user - uses "," as the delimiter

        newList = []  # Empty new list to store the provided tasks in the desired format - in this case that means removing leading whitespace
        for i in tasklist:
            newList.append(i.lstrip(' '))  # Removes leading white space and then adds task to the new list

        userLists = username + "_lists"  # Makes the name of the table created on sign up that stores all the user's lists

        # Inserts into new table the user id in order for the table to auto assign a list id for later use
        db.execute("INSERT INTO ? (user_id) VALUES (?)", userLists, session["user_id"])

        # Gets the newly assigned list id
        list_id = db.execute("SELECT list_id FROM ? WHERE list_table_name IS NULL", userLists)
        list_id = str(list_id[0]["list_id"])  # Extracts the list id from the returned list of dicts and converts it to a str
        listTableName = username + "_list_id_" + list_id  # Makes new table's name that will hold all tasks for this list

        # Adds the name of the new table to the table that holds a list of all of the user's lists
        db.execute("UPDATE ? SET list_table_name = ?, list_title = ? WHERE list_id = ?", userLists, listTableName, title, int(list_id))

        # Creates a new table to hold all of the new list's items
        db.execute("CREATE TABLE ? (row_id INTEGER PRIMARY KEY, list_id INTEGER, status INTEGER, task TEXT, comp_date TEXT, goal_date TEXT, FOREIGN KEY (list_id) REFERENCES ?(list_id))", listTableName, userLists)

        for item in newList:  # Inserts new list's items into the newly created table
            db.execute("INSERT INTO ? (list_id, task) VALUES (?, ?)", listTableName, int(list_id), item)

        # # Generate excel file
        # filePath = excel_generator(newList, title, username, listTableName)
        userListsInfo = db.execute("SELECT * FROM ?", userLists)
        return render_template("viewlists.html", username=username, listInfo=userListsInfo, active_page="Dashboard")
    else:
        return render_template("newlist.html", active_page="Dashboard")


# # Download file
# @app.route("/download", methods=["GET", "POST"])
# @login_required
# def download_file():
#     filepath = request.args.get("filepath")
#     print(f"\n\n\n{filepath}\n\n\n")

#     return send_file(filepath, as_attachment=True)


# Select the list chosen by user from viewlists
@app.route("/list_selector")
@login_required
def select_list():
    """Shows the list selected from the view list page"""
    # Gets the currect user's username
    username = db.execute("SELECT username FROM users WHERE user_id = ?", session["user_id"])
    username = username[0]["username"]  # Extracts the username string from the returned list of dicts
    listName = request.args.get("listname")

    listContent = db.execute("SELECT * FROM ?", listName)
    listID = listContent[0]["list_id"]
    userListsTable = username + "_lists"
    title = db.execute("SELECT list_title FROM ? WHERE list_id = ?", userListsTable, listID)
    title = title[0]["list_title"]

    return render_template("showfromview.html", tasklist=listContent, title=title, listname=listName)


# Save Changes to the list
@app.route("/save_list", methods=["POST"])
@login_required
def save_list():
    """Save changes to the list"""
    listName = request.form.get("listname")
    # print(f"\n\n\n{listName}\n\n\n")

    listContent = db.execute("SELECT * FROM ?", listName)
    # print(f"\n\n\n{listContent}\n\n\n")

    # for item in listContent:
    #     print(f"\n{item}\n")

    # for item in listContent:
    #     print(f"\n{item['row_id']}\n")

    # print(f"\n\n\n{request.form.get('status-1')}\n\n\n")
    # print(f"\n\n\n{request.form.get('comp_date-1')}\n\n\n")
    # print(f"\n\n\n{request.form.get('goal_date-1')}\n\n\n")

    for item in listContent:
        rowID = item['row_id']
        status = request.form.get(f"status-{item['row_id']}")
        comp_date = request.form.get(f"comp_date-{item['row_id']}")
        goal_date = request.form.get(f"goal_date-{item['row_id']}")

        db.execute("UPDATE ? SET status = ?, comp_date = ?, goal_date = ? WHERE row_id = ?", listName, status, comp_date, goal_date, rowID)

    return redirect("/view_lists")

    # listContent2 = db.execute("SELECT * FROM ?", listName)
    # for item in listContent2:
    #     print(item)

        # print(f"\n\n\nNEWNEWNEW{status}\n\n\n")
        # print(f"\n\n\nNEWNEWNEW{comp_date}\n\n\n")
        # print(f"\n\n\nNEWNEWNEW{goal_date}\n\n\n")

        # comp_date
        # goal_date

