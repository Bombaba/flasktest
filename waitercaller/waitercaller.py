import flask
import flask_login
from mocklogindb import MockLoginDB as LoginDB
from user import User
from passwordhelper import validate_password

DB = LoginDB()

app = flask.Flask(__name__)
app.secret_key = 'g%|m?EHF-5V%aujbjM{%|Mz##SG!xNzdWFGJT1mV'
login_manager = flask_login.LoginManager(app)

@app.route("/")
def home():
    return flask.render_template("home.html")

@app.route("/login", methods=["POST"])
def login():
    email = flask.request.form.get('email')
    password = flask.request.form.get('password')
    user = DB.get_user(email)
    if user and validate_password(password, user.salt, user.hash):
        flask_login.login_user(user, remember=True)
        return flask.redirect(flask.url_for('account'))
    else:
        return home()

@app.route("/register", methods=['POST'])
def register():
    email = flask.request.form.get('email')
    password = flask.request.form.get('password')
    password2 = flask.request.form.get('password2')
    if password != password2:
        return "Passwords unmatch."
    DB.add_user(email, password)
    return home()

@app.route("/logout")
def logout():
    flask_login.logout_user()
    return flask.redirect(flask.url_for('home'))

@app.route("/account")
@flask_login.login_required
def account():
    return "You are logged in"

@login_manager.user_loader
def load_user(user_id):
    return DB.get_user(user_id)

if __name__ == '__main__':
    app.run(port=8000, debug=True)
