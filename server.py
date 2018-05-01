import os
from flask_login import login_required, login_url, UserMixin, LoginManager, login_user, current_user

from flask import Flask, request, send_from_directory, Response, redirect, url_for, g, flash
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from functools import wraps

app = Flask(__name__)
app.debug = True
app.secret_key = "Whoop$"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

login_manager = LoginManager()
login_manager.init_app(app)

database = os.getcwd() + '/database.db'
engine = create_engine('sqlite:///' + database)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

#
#  LOGIN MANAGEMENT
#


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#
#  END LOGIN MANAGEMENT
#



# """
#    ROUTES
# """

@app.route('/')
def splash():
    return send_from_directory('static/html', "splash.html")


@app.route('/login', methods=['GET'])
def login_get():
    return send_from_directory('static/html', "login.html")


@app.route('/home')
@login_required
def home():
    return send_from_directory('static/html', "home.html")


@app.route('/profile')
def profile():
    return send_from_directory('static/html', "profile.html")


# """
#    END SPECIFIC PAGES
# """
#
# """
#    send_js and send_css will catch all requests
#    for css or js files as long as the inclusion
#    starts with /css or /js in the html:
#
#    CSS:
#    <link href="/css/YOUR_STYLE_SHEET.css" rel="stylesheet">
#
#    JS:
#    <script src="/js/YOUR_SCRIPT.js"></script>
# """


@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('static/js', path)


@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('static/css', path)


@app.route('/images/<path:path>')
def send_image(path):
    return send_from_directory('static/images', path)


# """
#    END CSS AND JAVASCRIPT
# """
#
# """
#    DATA ROUTES
# """


@app.route('/login', methods=['POST'])
def login_post():
    # Once we have a database we would check for the user
    # here and if they have the correct credentials, return a
    # token to put in the cookies. If they don't exist send that
    # as the response
    #
    # Opted to use flask login instead, handles a lot for us
    # use the current_user object
    username = request.form["user"]
    password = request.form["pass"]

    user = User.query.filter(User.username == username).first()
    if user is None or not user.check_password(password):
        flash('Invalid Login')
        return Response('Invalid Login')
    login_user(user)
    return Response('Nice, those are valid credentials!')


@app.route('/signup', methods=['POST'])
def signup():
    try:
        username = request.form["user"]
        password = request.form["pass"]
        if is_unique_name(username):
            new_user = create_new_user(username, password)
            login_user(new_user)
            return Response("Nice new login!")
        else:
            return Response("that shit taken")
    except KeyError:
        print("Missing parameter from request object.")
        return Response("Missing parameter from form.")
    except BaseException as err:
        print(err.args[0])

    return Response("OOPSIE WOOPSIE!! Uwu We made a fucky wucky!! A wittle fucko boingo! The code monkeys at our "
                    "headquarters are working VEWY HAWD to fix this!")


# """
#    END DATA ROUTES
# """
#
# """
# DB Objects
# """

# this is both flasks login object and the database user model
class User(Base, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=True)
    skills = Column(String(1000), unique=False, nullable=True)
    password = Column(String(20), unique=False, nullable=False)

    def check_password(self, password):
        user = User.query.filter_by(id=self.id).first()
        return password == user.password

    def __repr__(self):
        return '<User %r>' % self.username


class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True)
    title = Column(String(80), unique=True, primary_key=True)
    owner = Column(Integer, ForeignKey('users.id'), nullable=False)
    email = Column(String(120), unique=True, nullable=True)
    skills = Column(String(1000), unique=False, nullable=True)

    def __repr__(self):
        return '<Project %r>' % self.username


class Contributor(Base):
    __tablename__ = 'contributors'
    id = Column(Integer, primary_key=True)
    user = Column(Integer, ForeignKey('users.id'), nullable=False)
    project = Column(Integer, ForeignKey('projects.id'), nullable=True)

    def __repr__(self):
        return '<Item: %r: Contributor %r for project %r>' % self.id, self.user, self.project


# """
# End DB Objects
# """

# """
# DB Functions
# """

def init_db():
    Base.metadata.create_all(bind=engine)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


def get_users_projects(username):
    return


def is_unique_name(username):
    try:
        return User.query.filter(User.username == username).first() is None
    except BaseException as err:
        print(err.args[0])

    return False


def create_new_user(username, password):
    try:
        new_user = User(username=username, password=password, skills="I like to party!")
        db_session.add(new_user)
        db_session.commit()
        return new_user
    except BaseException as err:
        print(err.args[0])
        flash('Error creating new user.')
        return redirect(url_for('.login'))


def add_user_as_contributor(user_id, project_id):
    try:
        new_contributor = Contributor(user=user_id, project=project_id)
        db_session.add(new_contributor)
        db_session.commit()
        return new_contributor
    except BaseException as err:
        print(err.args[0])
        flash("Error adding user as contributor, please try again.")
        return redirect(url_for('.home'))


def create_new_project(title, user_id, email="", skills=""):
    try:
        new_project = Project(title=title, owner=user_id, email=email, skills=skills)
        db_session.add(new_project)
        db_session.commit()
    except BaseException as err:
        print(err.args[0])
        flash("Error adding user as contributor, please try again.")
        return redirect(url_for('.home'))


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)

    return decorated


def authenticate():
    # """Sends a 401 response that enables basic auth"""
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})


def check_auth(username, password):
    # make this shit use the db, we'll need to check authentication for editing projects based off a user owning them
    return True


if __name__ == '__main__':
    init_db()
    app.run()
