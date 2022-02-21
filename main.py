import atexit
from flask import Flask, request, jsonify
from Database import DatabaseWrapper
import os
from lib import load_dotenv


app = Flask(__name__, static_folder="static")
db = None


def error_response(code=500, msg="There was an error"):
    return jsonify({
        "code": code,
        "title": msg
    }), code


def ok_response(code=200, msg=""):
    return jsonify({
        "code": code,
        "title": msg
    }), code


# Validate a user's credentials
@app.route('/validate', methods=['POST'])
def login():
    correct = db.check_user(request.form['username'], request.form['password'])

    if correct:
        return ok_response(code=200, msg="User is valid")

    return error_response(code=404, msg="User not found")


# Insert a new user into the database
@app.route("/newuser", methods=['POST'])
def newuser():
    if db.user_exists(request.form['username']):
        # TODO: Return Error
        return error_response(code=403, msg="User already exists")

    if bool(request.form.getlist('IsAdmin')):
        if not db.new_user(request.form['username'], request.form['password'], True, request.form['passwordadmin']):
            return ok_response(code=201, msg="User created")
    else:
        db.new_user(request.form['username'], request.form['password'])

    return


if __name__ == '__main__':
    load_dotenv()

    production = bool(os.getenv("API_PRODUCTION"))
    port = int(os.getenv("API_PORT"))

    db_passwd = os.getenv("DB_PASSWD")
    db_name = os.getenv("DB_NAME")
    db_user = os.getenv("DB_USER")
    db_port = os.getenv("DB_PORT")
    db_host = os.getenv("DB_HOST")

    db = DatabaseWrapper(db_name=db_name, db_user=db_user, db_passwd=db_passwd, db_port=db_port, db_host=db_host)
    atexit.register(db.close)  # On clean exit, close the connections

    app.secret_key = os.urandom(12)

    app.run(host="0.0.0.0", port=port)  # Use for testing
