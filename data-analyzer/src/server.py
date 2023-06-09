from flask import *

from flask import Flask
from helpers import user_exists, summarize_category

app = Flask(__name__)

base_url = "/v1/summary"


@app.route(f"{base_url}/<user_id>/category")
def get_category_summary(user_id):
    if not user_exists(user_id):
        return make_response(jsonify({"message": "user does not exist"}), 404)

    summary = summarize_category(user_id=user_id, on="category")

    return jsonify(summary)


@app.route(f"{base_url}/<user_id>/sub_category")
def get_sub_category_summary(user_id):
    if not user_exists(user_id):
        return make_response(jsonify({"message": "user does not exist"}), 404)

    summary = summarize_category(user_id=user_id, on="sub_category")

    return jsonify(summary)


@app.route(f"{base_url}/<user_id>/merchant")
def get_merchant_summary(user_id):
    if not user_exists(user_id):
        return make_response(jsonify({"message": "user does not exist"}), 404)

    summary = summarize_category(user_id=user_id, on="merchant")

    return jsonify(summary)

@app.before_request
def basic_authentication():
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "*")
        response.headers.add("Access-Control-Allow-Methods", "*")
        return Response()
    
@app.after_request
def add_cors_header(response):
    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:8081'
    return response

if __name__ == "__main__":
    app.run(port=5000, host="0.0.0.0")
