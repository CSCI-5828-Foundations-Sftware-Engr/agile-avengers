import json
import logging
import os
import socket
import sys
import traceback
from datetime import datetime
from flask import Flask, abort, jsonify, render_template, request
from flask_cors import CORS
from werkzeug.exceptions import HTTPException
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine,MetaData
import sqlalchemy as db
import random
import string
from sqlalchemy.orm import sessionmaker


sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "./"))
from datamodel.models.userinfo import UserInfo
from config.constants import DB_CREDENTIALS


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
            request.headers.get("X-Remote-User"), request.headers.get("X-Firstname"), request.headers.get("-Lastname"),
        ),
        "message": "This is the default API endpoint",
    }

@app.route(api_url +'/userinfo/<user_id>', methods=['GET'])
def get_user_info(user_id):
    user = session.query(UserInfo).filter_by(user_id=user_id).first()
    if user:
        return jsonify({
            'first_name': user.first_name,
            'last_name': user.last_name,
            'mobile_number': user.mobile_number,
            'email': user.email_id,
            'is_merchant' : user.is_merchant,
            'created_on': user.created_on,
            'created_by' : user.created_by,
            'updated_on' : user.updated_on,
            'updated_by' : user.updated_by,

        })
    else:
        return jsonify({'message': 'User not found'})
    
# route to create random users

@app.route(api_url +'/create_users')
def create_users():
    for i in range(10):
        user_id = ''.join(random.choices(string.digits, k=5))
        first_name = ''.join(random.choices(string.ascii_lowercase, k=5))
        last_name = ''.join(random.choices(string.ascii_lowercase, k=5))
        mobile_number = ''.join(random.choices(string.digits, k=10))
        email_id = first_name.lower() + '.' + last_name.lower() + '@example.com'
        is_merchant = True
        created_on = datetime.now()
        created_by = user_id
        updated_on = datetime.now()
        updated_by = user_id

        # create a new user
        user = UserInfo(
            user_id=user_id,
            first_name=first_name,
            last_name=last_name,
            mobile_number=mobile_number,
            email_id=email_id,
            is_merchant=is_merchant,
            created_on=created_on,
            created_by=created_by,
            updated_on=updated_on,
            updated_by=updated_by
        )

        # add the user to the session
        session.add(user)

    # commit the changes
    session.commit()

    return jsonify({'message': '10 users created successfully'})
    
# route to update user_info

@app.route(api_url +'/update_userinfo/<user_id>')
def update_user_info(user_id):
    data=request.json()
    user = session.query(UserInfo).filter_by(user_id=user_id).first()
    if user:
        
            user.first_name =data["first_name"]
            user.last_name = data["last_name"]
            user.mobile_number= data["mobile_number"]
            user.email_id= data["email_id"]
            # 'is_merchant' : user.is_merchant,
            # 'created_on': user.created_on,
            # 'created_by' : user.created_by,
            user.updated_on =datetime.now() 
            user.updated_by =user_id
            return jsonify({
            'first_name': user.first_name,
            'last_name': user.last_name,
            'mobile_number': user.mobile_number,
            'email': user.email_id,
            'is_merchant' : user.is_merchant,
            'created_on': user.created_on,
            'created_by' : user.created_by,
            'updated_on' : user.updated_on,
            'updated_by' : user.updated_by,

        })   
        
    else:
        return jsonify({'message': 'User not found'})    
    




    
    

