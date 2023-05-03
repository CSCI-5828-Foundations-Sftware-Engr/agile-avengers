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


if __name__ == "__main__":
    app.run(port=5000, host="0.0.0.0")
