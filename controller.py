import hashlib
import db_handler
import encryption_helper

conn = db_handler.connect('db.db')
db_handler.check_tables(conn)


def add_password(name, password, key, user):
    result = db_handler.query_single_password(conn, user, name)
    if result:
        return False, 'password for this platform already exists'
    if len(name) < 2:
        return False, 'name of the platform is too short'
    if len(password) < 6:
        return False, 'password is too short'

    nonce, cipertext, tag = encryption_helper.encrypt(key.encode(), password)
    db_handler.add_password(conn, name, cipertext, nonce, tag, user)
    return True, ''


def get_passwords(username):
    passwords = db_handler.get_user_passwords(conn, username)
    if len(passwords) == 0:
        return False, 'No registered passwords'
    return True, passwords


def reveal_password(passwordHash, nonce, tag, key):
    check, text = encryption_helper.decrypt(key.encode(), passwordHash, nonce, tag)
    if not check:
        return False, text
    return True, text.decode()


def login(username, password):
    results = db_handler.get_user(conn, username)
    if not results:
        return False, 'no user'

    db_user, db_password = results[0]

    if hashlib.sha256(password.encode()).hexdigest() == db_password:
        return True, ''
    return False, 'wrong password'


def create_account(username, password):
    if len(password) > 16:
        return False, 'password must be 16 or less characters'
    check, _ = get_user(username)
    if check:
        return False, 'User already Exists'

    if len(password) < 16:
        return False, 'password should be 16 characters long'
    password = hashlib.sha256(password.encode()).hexdigest()
    db_handler.add_user(conn, username, password)
    return True, ''


def get_user(username):
    user = db_handler.get_user(conn, username)
    if len(user) == 0:
        return False, 'No user'
    return True, user
