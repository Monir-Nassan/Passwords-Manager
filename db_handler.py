import sqlite3
from sqlite3 import Connection


def connect(database):
    return sqlite3.connect(database)


def check_tables(conn):
    curr = conn.cursor()
    curr.execute('SELECT name FROM sqlite_master WHERE type="table" AND name="users"')
    users_table = curr.fetchone()
    if not users_table:
        create_users_table(conn)
    curr.execute('SELECT name FROM sqlite_master WHERE type="table" AND name="passwords"')
    passwords_table = curr.fetchone()
    if not passwords_table:
        create_passwords_table(conn)


def delete_password(conn, name, username):
    curr = conn.cursor()
    x = curr.execute('delete from passwords where name=:name and user=:username',{'name':name,
                                                                              'username':username})

    conn.commit()

def create_users_table(con):
    cur = con.cursor()
    cur.execute('''CREATE TABLE users
                   (username text, password text)''')


def create_passwords_table(con):
    cur = con.cursor()
    cur.execute('''CREATE TABLE passwords
                   (name text, 
                   password text, 
                   iv text, 
                   user text,
                   FOREIGN KEY (user)
                   REFERENCES users (username) )''')


def query_single_password(conn, user, platform):
    cur = conn.cursor()
    cur.execute('''select * from passwords where user=:user and name=:name''', {'user': user,
                                                                                'name': platform})
    return cur.fetchone()

def add_user(con, username, password):
    cur = con.cursor()
    cur.execute("INSERT INTO users VALUES (?, ?)", (username, password))
    con.commit()


def get_user(con: Connection, username):
    cur = con.cursor()
    cur.execute("select * from users where username=:username", {'username': username})
    return cur.fetchall()


def get_user_passwords(con: Connection, username):
    cur = con.cursor()
    cur.execute("select * from passwords where user=:username", {'username': username})
    results = cur.fetchall()

    return results


def add_password(con: Connection,
                 name,
                 password,
                 iv,
                 user):
    cur = con.cursor()
    cur.execute("INSERT INTO passwords VALUES (?, ?, ?, ?)", (name, password, iv, user))
    con.commit()
