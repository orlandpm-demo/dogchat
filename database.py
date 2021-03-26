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

def get_all_posts(handle):
    print('query')
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)

    cursor = conn.cursor()
    cursor.execute("""
SELECT 
    Posts.Id,
    Posts.Handle, 
    Posts.Text,
    Dogs.Name,
    Dogs.AvatarImageName,
    LikeCountQueryResult.LikeCount,
    DL.CurrentDogLike

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

INNER JOIN (SELECT Posts.Id AS Id, COUNT(L.Handle) AS CurrentDogLike FROM Posts
    LEFT JOIN (SELECT * FROM Likes WHERE Handle=?) AS L 
        ON Posts.Id = L.PostId
    GROUP BY Posts.Id) AS DL
    ON Posts.Id = DL.Id
""", handle)

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


    
def get_comments(post_id):
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = conn.cursor()
    cursor.execute("SELECT [Handle], [Text] FROM Comment WHERE PostId = ?", post_id)
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


def like_count(post_id):
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM Likes WHERE PostId = ?", post_id)
    for row in cursor:
        return row[0]

def already_liked(handle, post_id):
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM Likes WHERE PostId = ? AND Handle = ?", post_id, handle)
    for row in cursor:
        return (row[0] > 0)

def like_post(handle, post_id):
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = conn.cursor()
    result = cursor.execute("""INSERT INTO Likes (Handle, PostId) VALUES (?, ?)""", handle, post_id)
    conn.commit()
    print(result)

def unlike_post(handle, post_id):
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = conn.cursor()
    result = cursor.execute("""DELETE FROM Likes WHERE Handle = ? AND PostId = ?""", handle, post_id)
    conn.commit()
    print(result)

def toggle_like(handle, post_id):
    if already_liked(handle,post_id):
        action = 'unlike'
        unlike_post(handle,post_id)
    else:
        action = 'like'
        like_post(handle,post_id)
    return {
        'like_count' : like_count(post_id),
        'action': action
    }

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