import sys

from flask_app import app as application

activate_this = "/app/easy-pay/server/venv/bin/activate_this.py"
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))
sys.path.insert(0, "/app/easy-pay/server")
application.secret_key = "anything you wish"
