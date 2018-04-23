from flask import Flask, request, send_from_directory, Response, redirect, url_for

app = Flask(__name__)

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
    return Response("yeet")

@app.route('/signup', methods=['POST'])
def signup():
    # Once we have a database we will want to make this create
    # a new user
    username = request.form["user"]
    password = request.form["pass"]
    return Response("yeet")
"""
   END DATA ROUTES
"""



if __name__ == '__main__':
    app.run()
