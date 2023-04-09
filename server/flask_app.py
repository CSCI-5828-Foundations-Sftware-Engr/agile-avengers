import json
import logging
import os
import socket
import sys
import traceback
from datetime import datetime
import sqlalchemy
from sqlalchemy.orm import sessionmaker

from flask import Flask, abort, jsonify, render_template, request, make_response


from flask_cors import CORS
from werkzeug.exceptions import HTTPException

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../"))

from helpers.user_management import create_new_user, user_login, user_logout, check_userinfo
from datamodel.models.userinfo import UserInfo

app = Flask(
    __name__,
    static_folder="../client",
    template_folder="../client",
    # static_url_path="",
)
api_url = "/api/v1/"
CORS(app)

engine = sqlalchemy.create_engine("postgresql://postgres:password@localhost:5432/agile_avengers")
Session = sessionmaker(engine)

if __name__ != "__main__":
    gunicorn_error_logger = logging.getLogger("gunicorn.error")
    app.logger.handlers.extend(gunicorn_error_logger.handlers)
    app.logger.setLevel(logging.INFO)
# gunicorn_logger = logging.getLogger("gunicorn.error")
# app.logger.handlers = gunicorn_logger.handlers
# app.logger.setLevel(gunicorn_logger.level)


@app.errorhandler(Exception)
def resource_not_found(e):
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    try:
        error_object = {"error": {"status_code": code, "message": str(e).split(":", 1)[1].strip()}}
    except Exception as error:
        app.logger.info("Failed to parse the error message - {}".format(str(error)))
        error_object = e
    app.logger.info(
        "username - {}. This is the value of error object - {}".format(
            request.headers.get("X-Remote-User"), error_object
        )
    )
    return jsonify(error_object), code


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def catch_all(path):
    return render_template("index.html")


@app.route(api_url + "/get_current_time")
def get_current_time():
    return {
        "status": "Welcome - {}\nFull name - {} {}".format(
            request.headers.get("X-Remote-User"),
            request.headers.get("X-Firstname"),
            request.headers.get("-Lastname"),
        ),
        "message": "This is the default API endpoint",
    }


@app.route(api_url + "/userinfo/<int:user_id>", methods=["GET"])
def get_user_info(user_id):
    user = db.query.filter_by(id=user_id).first()
    if user:
        return jsonify(
            {
                "first_name": user.first_name,
                "last_name": user.last_name,
                "mobile_number": user.mobile_number,
                "email": user.email_id,
                "is_merchant": user.is_merchant,
                "created_on": user.created_on,
                "created_by": user.created_by,
                "updated_on": user.updated_on,
                "updated_by": user.updated_by,
            }
        )
    else:
        return jsonify({"message": "User not found"})


base_route = f"/api/v1/auth"


@app.route(f"{base_route}/create", methods=["POST"])
def create_user():
    user_data = request.json

    # Add to userinfo table
    ui = UserInfo(user_id=user_data["username"])
    try:
        with Session() as session:
            print("adding userinfo")
            session.add(ui)
            session.commit()
    except Exception as e:
        print(e)
        make_response(jsonify({"message": "Server Error"}), 500)

    new_user = create_new_user(user_data["username"], user_data["password"])
    print(new_user)
    if new_user is None:
        return make_response(jsonify({"message": "user already exists"}), 409)

    return jsonify({"message": "user created"})


@app.route(f"{base_route}/login", methods=["POST"])
def login():
    user_data = request.json
    token = user_login(user_data["username"], user_data["password"])
    resp = make_response(jsonify({"message": "logged in successfully"}), 200)
    for key, value in token.items():
        resp.set_cookie(key, json.dumps(value))
    resp.set_cookie("auth_token", json.dumps(token))
    return resp


@app.route(f"{base_route}/logout", methods=["POST"])
def logout():
    token = request.cookies.get("refresh_token")
    user_logout(token)
    return jsonify({"message": "logged out"})


@app.route(f"{base_route}/userinfo")
def userinfo():
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")
    auth_token = {"access_token": access_token, "refresh_token": refresh_token}
    token, userinfo = check_userinfo(auth_token)

    if userinfo is not None:
        resp = make_response(jsonify({"userinfo": userinfo}), 200)
        resp.set_cookie("auth_token", json.dumps(token))
        resp.set_cookie("access_token", json.dumps(token["access_token"]))
        resp.set_cookie("refresh_token", json.dumps(token["refresh_token"]))
        return resp

    return make_response(jsonify({"message": "Unauthorized"}), 403)


if __name__ == "__main__":
    app.run(port=5000, host="localhost")
