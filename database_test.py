import pyodbc 

import pyodbc 
# Some other example server values are
# server = 'localhost\sqlexpress' # for a named instance
# server = 'myserver,port' # to specify an alternate port
server = 'tcp:dogchatserver.database.windows.net' 
database = 'dogchat' 
username = 'dogchatadmin' 
password = 'R0ver123$' 

def get_dogs():
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = cnxn.cursor()
    cursor.execute('SELECT * FROM Dogs')
    return [row for row in cursor]



# conn_string = """Driver={ODBC Driver for SQL Server 17};Server=tcp:dogchatserver.database.windows.net,1433;Initial Catalog=dogchat;Persist Security Info=False;User ID=dogchatadmin;Password=R0ver123$;MultipleActiveResultSets=False;Encrypt=True;TrustServerCertificate=False;Connection Timeout=30;"""
# conn = pyodbc.connect(conn_string)
# # conn = pyodbc.connect('Driver={SQL Server};'
# #                       'Server=dogchatserver.database.windows.net;'
# #                       'Database=dogchat;'
# #                       'Password=R0ver123$;'
# #                       'Trusted_Connection=yes;')

# cursor = conn.cursor()


