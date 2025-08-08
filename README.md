# Class List - A List Making Web Application
#### Video Demo: https://youtu.be/1OjZTHI2I8A
#### Description:
Welcome to Class List. Class list is a web application developed using the Flask micro-framework along with Bootstrap for CSS to assist users in making quick and simple task lists. Keeping track of what needs to be done, whether it’s at school, work, or at home, can be difficult. When faced with such an issue one might decide to search for an application that can assist with keeping tasks organized and tracked. That is where Class List comes in. Class list is designed to be easy to use, while also delivering the features one needs to track necessary tasks. Below is a detailed overview of all files contained in the project folder submitted. Starting with the files directly in the “project” folder. Then followed by the folders named “static” and “templates” and the files they contain.


**File:** app.py\
**Location:** /project/\
**Description:**\
This is the main application code written in python using the Flask framework. It utilizes the following libraries. Flask, flask_session, cs50, werkzeug.security, helpers, and datetime. This .py program controls how the application functions and contains the code to perform all major server-side processing. A key part of this file is it contains the list generating code as well as all of the database handling to save user content. This file can redirect the user to any part of the web application and process all user requests.

**File:** classlist.db\
**Location:** /project/\
**Description:**\
This is the database file. This file contains all user information that is needed to run their session. It also stores their lists and their current progress on each so that a user can close their browser and return at a later date. This database was implemented using SQLite3 and the cs50 python library.

**File:** helpers.py\
**Location:** /project/\
**Description:**\
Contains a decorator that makes sure the user is logged in before accessing certain parts of the application as well as the error handling function.

**File:** README.md\
**Location:** /project/\
**Description:**\
This README.md file containing project details.

**Folder:** static\
**Location:** /project/\
**Description:**\
This folder contains the styles.css file as well as different assets used throughout the application such as images.

**Folder:** site-preview-slides\
**Location:** /project/static/
**Description:**\
This folder is inside the static folder and contained the images used in the site preview carousel found on the landingpage.html file of the application.

**File:** loan-7AIDE8PrvA0-unsplash.jpg\
**Location:** /project/static/
**Description:**\
Image of a hissing cat used in the error.html file to add some humor to error messages. Image Credit “Photo by Loan on Unsplash”.

**File:** static.css\
**Location:** /project/static/
**Description:**\
CSS file used to implement custom CSS. This project utilized Bootstrap for most of its CSS. However, when custom styling or formatting was needed, it was implemented using this file.

**File:** ui-checks.svg\
**Location:** /project/static/
**Description:**\
Small icon from Bootstrap used as the sites logo.

**Folder:** templates\
**Location:** /project/\
**Description:**\
This folder contains all of the projects HTML templates which are accessed via the app.py file.

**File:** about.html\
**Location:** /project/templates/\
**Description:**\
This page provides the user with some basic information about the web application.

**File:** changepassword.html\
**Location:** /project/templates/\
**Description:**\
This page is rendered when the user wants to change their password. This page allows this by having the user enter their current password once followed by their new password twice. This page then sends this information to the app route “/change_password” where the information is checked. If the current password is correct and the new password fields match, the password is changed by updating the password_hash field of the users table in the database.

**File:** deleteaccount.html\
**Location:** /project/templates/\
**Description:**\
This page allows the user to delete their account. It displays a form that asked the user to enter their password twice. This information is then sent to the app route “/delete_account” where it is checked. If the password fields match and are the correct password. The user is deleted by first deleting all tables belonging to the user then by removing the user form the list of users.

**File:** deletionconfirmation.html\
**Location:** /project/templates/\
**Description:**\
Displays a message if account deletion was successful.

**File:** error.html\
**Location:** /project/templates/\
**Description:**\
Displays error messages depending on the error.

**File:** index.html\
**Location:** /project/templates/\
**Description:**\
This page serves as a logged in user’s homepage. This is where their “dashboard” is show. From here they can elect to make a new list or view their current lists. Whichever they chose will trigger the appropriate app route that will take the user to the page where they can perform the desired action.

**File:** landingpage.html\
**Location:** /project/templates/\
**Description:**\
This is the homepage for users not logged in. It shows the option “log In” and “Sign Up” along with an auto playing carousel that shows a preview of how the web application works.

**File:** layout.html\
**Location:** /project/templates/\
**Description:**\
This is the main layout file. All other HTML files extend this main layout file. This file implements the nav bar, the main background color, and the footer.

**File:** login.html\
**Location:** /project/templates/\
**Description:**\
This is where the user may log in if they already have an account. There is a button that will redirect them to the “Sign Up” page if they do not have an account. If the user attempts to log in, the provided information will be processed by the “/login” app route and only if the information provided matches a current user will the user be logged in. If not, an error message will be displayed.

**File:** myaccount.html\
**Location:** /project/templates/\
**Description:**\
This page displayed the user’s account information. This information is draw from the database and sent to this page for display.

**File:** newlist.html\
**Location:** /project/templates/\
**Description:**\
This page displays the form that users utilize to generate a new list. Once a user submits the form the information is sent to the “/new_list” app route where the data is processed.

**File:** showfromview.html\
**Location:** /project/templates/\
**Description:**\
This page displays the list the user selected from the viewlists.html page.

**File:** signup.html\
**Location:** /project/templates/\
**Description:**\
This page allows the user to sign up for an account. After the user submits the requested information the “/signup” app route is triggered. If the provided information meets the sign-up requirements, the database is updated with the new user’s information.

**File:** viewlists.html\
**Location:** /project/templates/\
**Description:**\
This page displays the user’s lists and allows for the section of one to open for viewing or editing.

\
This application was made to fulfill the requirements of the final project for the course titled CS50x from HarvardX.
