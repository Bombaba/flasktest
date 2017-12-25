from dbcrime import DBCrime
import flask
import dbconfig


app = flask.Flask(__name__)
DB = DBCrime()

@app.route("/")
def home():
    data = None
    data = DB.get_all_inputs()
    return flask.render_template("home.html",
                                 data=data,
                                )

@app.route("/add", methods=['POST'])
def add():
    data = flask.request.form.get("userinput")
    if data:
        DB.add_input(data)
    return home()

@app.route("/clear")
def clear():
    DB.clear_all()
    return home()

if __name__ == '__main__':
    app.run(port=8000, debug=True)
