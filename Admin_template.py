
"""
Rename this file to Admin.py
Enter the appropriate credentials into the different credential classes

The purpose of this file is to store the sensitive passwords in a separate file not shared on GitHub
That way the public cannot see the location of the database/web-server, and cannot see the passwords
for them.
"""

class MySQLCredentials:
    host = 'database_host'
    database = 'database_name'
    user = 'user_name'
    password = 'database_password'

class GoogleSheetCredentials:
    json = 'LOCATION OF JSON GSPREAD CREDENTIALS'
    name = 'NAME OF GOOGLE SHEET'
    url = 'URL OF GOOGLE SHEET'



