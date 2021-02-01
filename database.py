import pyodbc 
from secrets import server, database, username, password
# conn = pyodbc.connect('Driver={SQL Server};'
#                       'Server=server_name;'
#                       'Database=database_name;'
#                       'Trusted_Connection=yes;')


def get_all_posts():
    print('query')
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)

    cursor = conn.cursor()
    cursor.execute("""
                        
                        SELECT 
                                Posts.Handle, 
                                Posts.Text,
                                Dogs.Name,
                                LikeCountQueryResult.LikeCount

                        FROM Posts

                        INNER JOIN Dogs
                                ON Posts.Handle = Dogs.Handle

                        INNER JOIN (SELECT 
                                Posts.Id,
                                -- Posts.Handle, 
                                -- Posts.Text, 
                                -- Dogs.Name,
                                COUNT(Likes.Handle) AS LikeCount
                            FROM Posts
                            
                            LEFT JOIN Likes
                                ON Posts.Id = Likes.PostId
                            GROUP BY Id) LikeCountQueryResult
                                ON LikeCountQueryResult.Id = Posts.ID
""")

    columns = [column[0] for column in cursor.description]

    results = []

    for row in cursor:
        d = dict(zip(columns,row))
        results.append(d)

    return results

def get_dog_by_handle(handle):
    print('query')
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Dogs WHERE Handle = ?", handle)

    columns = [column[0] for column in cursor.description]

    results = []

    for row in cursor:
        d = dict(zip(columns,row))
        results.append(d)

    if len(results) > 0:
        return results[0]
    else:
        return None

    
def get_posts_by_handle(handle):
    print('query')
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Posts WHERE Handle = ?", handle)

    columns = [column[0] for column in cursor.description]

    results = []

    for row in cursor:
        d = dict(zip(columns,row))
        results.append(d)

    return results