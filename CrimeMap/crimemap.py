import dateparser
import flask
import dbconfig
import json
from dbcrime import DBCrime

app = flask.Flask(__name__)
DB = DBCrime()

@app.route("/")
def home(error_message=None):
    crimes = DB.get_all_crimes()
    crimes = json.dumps(crimes)
    return flask.render_template(
        "home.html",
        map_key=dbconfig.gmap_key,
        crimes=crimes,
        categories=DBCrime.categories,
        error_message=error_message,
    )

@app.route("/submitcrime", methods=['POST'])
def submitcrime():
    category = flask.request.form.get("category")
    date = flask.request.form.get("date")
    latitude = flask.request.form.get("latitude")
    longitude = flask.request.form.get("longitude")
    description = flask.request.form.get("description")
    err = DB.add_crime(category, date, latitude, longitude, description)
    return home(err)

if __name__ == '__main__':
    app.run(port=8000, debug=True)
