from flask import redirect, render_template, session
from functools import wraps
# import xlsxwriter

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/landingpage")
        return f(*args, **kwargs)

    return decorated_function

def error_handling(message, code):
    return render_template("error.html", message=message, code=code)

# def excel_generator(taskList, title, username, listName):
#     # generate excel sheet here
#     filePath =
#     workbook = xlsxwriter.Workbook(filePath)
#     worksheet = workbook.add_worksheet(title)

#     bold = workbook.add_format({'bold': True})

#     worksheet.write(0, 0, 'Status', bold)
#     worksheet.write(0, 1, 'Task', bold)
#     worksheet.write(0, 2, 'Completion Date', bold)
#     worksheet.write(0, 3, 'Completion Goal', bold)

#     for i, item in enumerate(taskList):
#         worksheet.write(i + 1, 1, item)

#     workbook.close()

#     return filePath

