import datetime
import flask
import flask_login
import config
from user import User
from passwordhelper import validate_password
from forms import RegistrationForm, LoginForm, CreateTableForm

if config.test:
    from mocklogindb import MockLoginDB as DataBase
else:
    from mongohelper import MongoHelper as DataBase

DB = DataBase(config.DB_NAME)

app = flask.Flask(__name__)
app.secret_key = 'g%|m?EHF-5V%aujbjM{%|Mz##SG!xNzdWFGJT1mV'
login_manager = flask_login.LoginManager(app)

@app.route("/")
def home():
    return flask.render_template(
        "home.html", loginform=LoginForm(),
        registrationform=RegistrationForm()
    )

@app.route("/login", methods=["POST"])
def login():
    form = LoginForm(flask.request.form)
    if form.validate():
        user = DB.get_user(form.email.data)
        if user and validate_password(form.password.data, user.salt, user.hash):
            flask_login.login_user(user, remember=True)
            return flask.redirect(flask.url_for('account'))
        else:
            form.email.errors.append("Email or password invalid")
    return flask.render_template(
        "home.html", loginform=form,
        registrationform=RegistrationForm()
    )

@app.route("/register", methods=['POST'])
def register():
    form = RegistrationForm(flask.request.form)
    if form.validate():
        if DB.get_user(form.email.data):
            form.email.errors.append("email address already registered")
            return flask.render_template('home.html', registrationform=form)
        DB.add_user(form.email.data, form.password.data)
        return flask.render_template(
            "home.html", loginform=LoginForm(),
            registrationform=form,
            onloadmessage="Registration successful. Please log in.")
    return flask.render_template(
        "home.html", loginform=LoginForm(),
        registrationform=form
    )

@app.route("/logout")
def logout():
    flask_login.logout_user()
    return flask.redirect(flask.url_for('home'))

@app.route("/dashboard")
@flask_login.login_required
def dashboard():
    now = datetime.datetime.now()
    requests = DB.get_requests(flask_login.current_user.get_id())
    for req in requests:
        deltaseconds = (now - req['time']).seconds
        req['wait_minutes'] = f"{deltaseconds // 60}:{deltaseconds % 60:02}"
    return flask.render_template("dashboard.html", requests=requests)

@app.route("/account")
@flask_login.login_required
def account():
    return flask.render_template(
        "account.html", createtableform=CreateTableForm(),
        tables=DB.get_tables(flask_login.current_user.get_id())
    )

@app.route("/account/createtable", methods=["POST"])
@flask_login.login_required
def account_createtable():
    form = CreateTableForm(flask.request.form)
    if form.validate():
        DB.add_table(form.tablename.data, flask_login.current_user.get_id())
        return flask.redirect(flask.url_for('account'))
    return flask.render_template(
        "account.html", createtableform=form,
        tables=DB.get_tables(flask_login.current_user.get_id())
    )

@app.route("/account/deletetable")
@flask_login.login_required
def account_deletetable():
    table_id = flask.request.args.get("tableid")
    DB.delete_table(table_id)
    return flask.redirect(flask.url_for('account'))

@app.route("/dashboard/resolve")
@flask_login.login_required
def dashboard_resolve():
    request_id = flask.request.args.get("request_id")
    DB.delete_request(request_id)
    return flask.redirect(flask.url_for('dashboard'))

@app.route("/newrequest/<table_id>")
def new_request(table_id):
    if DB.add_request(table_id, datetime.datetime.now()):
        return "Your request has been logged and a waiter will be with you shortly."
    return "There is already a request pending for this table. Please be patient, a waiter will be there ASAP."


@login_manager.user_loader
def load_user(user_id):
    return DB.get_user(user_id)

if __name__ == '__main__':
    app.run(port=8000, debug=True)
