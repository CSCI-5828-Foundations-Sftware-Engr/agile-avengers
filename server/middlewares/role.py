from functools import wraps

from flask import jsonify, make_response, request

from db_queries import get_user_details


def role_middleware(func):
    @wraps(func)
    def __role_decorator(*args, **kwargs):
        try:
            username = request.headers.get("X-Remote-User")
            firstname = request.headers.get("X-Firstname")
            last_name = request.headers.get("X-Lastname")
            user_email = request.headers.get("X-Remote-User-Email")
            user_details = get_user_details(username, firstname, last_name, user_email)
            request.permission = user_details
            return func(*args, **kwargs)
        except Exception as e:
            return make_response(jsonify({"status": "failure", "reason": str(e)}), 401)

    return __role_decorator


def admin_authorizer_middleware(func):
    @wraps(func)
    def __decorator(*args, **kwargs):
        username = request.headers.get("X-Remote-User")
        firstname = request.headers.get("X-Firstname")
        last_name = request.headers.get("X-Lastname")
        user_email = request.headers.get("X-Remote-User-Email")
        user_details = get_user_details(username, firstname, last_name, user_email)
        if user_details["role"] != "admin":
            return make_response(jsonify({"status": "failure", "reason": "Not a admin user"}), 401)
        request.permission = user_details
        return func(*args, **kwargs)

    return __decorator
