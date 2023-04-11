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
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine,MetaData
import sqlalchemy as db
import random
import string

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../"))

from helpers.user_management import create_new_user, user_login, user_logout, check_userinfo
from datamodel.models.userinfo import UserInfo

app = Flask(
    __name__,
    static_folder="../client",
    template_folder="../client",
    # static_url_path="",
)



#connecting to postgres database
DATABASE_URI = "postgresql://{}:{}@{}/{}".format(
    DB_CREDENTIALS["USERNAME"], DB_CREDENTIALS["PASSWORD"], DB_CREDENTIALS["HOSTNAME"], DB_CREDENTIALS["DB_NAME"],
)
engine=create_engine(DATABASE_URI)
Session =sessionmaker(bind=engine)
session=Session()




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



