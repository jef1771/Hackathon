from flask import Flask, request, send_from_directory, Response, redirect, url_for, g
from functools import wraps
import sqlite3
import sys
import logging

app = Flask(__name__)
DATABASE = 'database.db'

"""
   ADD ROUTES HERE FOR SPECIFIC PAGES
"""


@app.route('/')
def splash():
    return send_from_directory('static/html', "splash.html")


@app.route('/login')
def login():
    return send_from_directory('static/html', "login.html")


@app.route('/home')
def home():
    return send_from_directory('static/html', "home.html")


@app.route('/home')
def profile():
    return send_from_directory('static/html', "profile.html")


"""
   END SPECIFIC PAGES
"""

"""
   send_js and send_css will catch all requests
   for css or js files as long as the inclusion
   starts with /css or /js in the html:

   CSS:
   <link href="/css/YOUR_STYLE_SHEET.css" rel="stylesheet">

   JS:
   <script src="/js/YOUR_SCRIPT.js"></script>
"""


@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('static/js', path)


@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('static/css', path)


@app.route('/images/<path:path>')
def send_image(path):
    return send_from_directory('static/images', path)


"""
   END CSS AND JAVASCRIPT
"""

"""
   DATA ROUTES
"""


@app.route('/login', methods=['POST'])
def login_post():
    # Once we have a database we would check for the user
    # here and if they have the correct credentials, return a
    # token to put in the cookies. If they don't exist send that
    # as the response
    username = request.form["user"]
    password = request.form["pass"]
    return send_from_directory('home.html')


@app.route('/signup', methods=['POST'])
def signup():
    try:
        conn = get_connection()
        email = "fuck"
        username = request.form["user"]
        password = request.form["pass"]
        if is_unique_name(conn, username):
            create_new_user(conn, email, username, password)
            return "u all signed in!"
        else:
            return Response("that shit taken")
    except KeyError:
        print("Missing parameter from request object.")
        return Response("Missing parameter from form.")
    except BaseException as err:
        print(err.args[0])
    finally:
        close_connection()

    return Response(
        "OOPSIE WOOPSIE!! Uwu We made a fucky wucky!! A wittle fucko boingo! The code monkeys at our headquarters are working VEWY HAWD to fix this!")


"""
   END DATA ROUTES
"""

"""
DB
"""


def is_unique_name(conn, username):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM users WHERE username = ?", (username,))
        username_exists = cursor.fetchall()
        if not username_exists:
            username_exists = 0
    except BaseException as err:
        print(err.args[0])

    return username_exists == 0


def create_new_user(conn, email, username, password):
    try:
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO users (email, username, password, skills) VALUES (?, ?, ?, ?)''',
                       (email, username, password, "I like to party!"))
        conn.commit()
    finally:
        cursor.close()


def get_connection():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        init_db(db)
    return db


def close_connection():
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def init_db(db):
    with app.app_context():
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


def query_db(query, args=(), one=False):
    cur = get_connection().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)

    return decorated


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})


def check_auth(username, password):
    # make this shit use the db, we'll need to check authentication for editing projects based off a user owning them
    return True


if __name__ == '__main__':
    app.run()
