import pyodbc 
from secrets import server, database, username, password
# conn = pyodbc.connect('Driver={SQL Server};'
#                       'Server=server_name;'
#                       'Database=database_name;'
#                       'Trusted_Connection=yes;')


def get_conn():
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    return conn

def make_avatar_url(avatar_image_name):
    return 'https://dogchatstorage.blob.core.windows.net/dogavatars/' + avatar_image_name

def get_all_posts():
    print('query')
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)

    cursor = conn.cursor()
    cursor.execute("""
                        
                        SELECT 
                                Posts.Handle, 
                                Posts.Text,
                                Posts.Id,
                                Dogs.Name,
                                Dogs.AvatarImageName,
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
        d['avatar_url'] = make_avatar_url(d['AvatarImageName'])
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


def insert_post(handle, post_content):
    print('query')
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)

    cursor = conn.cursor()
    result = cursor.execute("""INSERT INTO Posts ([Handle], [Text])
                        VALUES (?, ?)""", handle, post_content)
    conn.commit()
    print(result)

def delete_post(post_id, handle):
    print('delete query')
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)

    cursor = conn.cursor()
    result = cursor.execute("""DELETE FROM Posts WHERE Id= ? AND Handle= ?""", post_id, handle)
    conn.commit()
    print(result)

def create_user(username, name, bio, age, password_hash, avatar_image_name):
    conn = get_conn()
    cursor = conn.cursor()
    result = cursor.execute("""INSERT INTO Dogs ([Handle], [Name], [Bio], [Age], [PasswordHash], [AvatarImageName])
                        VALUES (?, ?, ?, ?, ?, ?)""", username, name, bio, age, password_hash, avatar_image_name)
    conn.commit()
    print(result)

def reset_database_password(username, password_hash):
    conn = get_conn()
    cursor = conn.cursor()
    result = cursor.execute("""UPDATE Dogs SET PasswordHash=? WHERE Handle=?""", password_hash, username)
    conn.commit()
    print(result)