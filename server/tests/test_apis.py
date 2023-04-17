from datamodel.models.userinfo import Base, UserInfo
from db_queries import session, engine
from flask_app import app
from unittest import mock


class TestBlog:
    def setup_class(self):
        Base.metadata.create_all(engine)
        self.session = session
        self.app_client = app.test_client()
        self.user_data = {
            "user_name": "preetham",
            "first_name": "Preetham",
            "last_name": "Maiya",
            "mobile_number": "1234566789",
            "email_id": "prma6536@colorado.edu",
            "is_merchant": False,
            "created_by": "preetham",
            "updated_by": "preetham",
        }

    def teardown_class(self):
        self.session.rollback()
        self.session.close()

    def test_base_endpoint(self):
        res = self.app_client.get("/")
        assert res.status_code == 200
        assert res.json == {"Test": "ok"}

    @mock.patch("flask_app.create_new_user")
    def test_create_user(self, mock_create_new_user):
        url = "/v1/auth/create"
        data = {"username": "preetham", "password": "password"}

        # Happy path
        mock_create_new_user.return_value = data
        res = self.app_client.post(url, json=data)
        assert res.status_code == 200

        users = (
            self.session.query(UserInfo).filter(UserInfo.user_name == "preetham").all()
        )
        assert len(users) == 1

        # Cleanup
        self.session.query(UserInfo).filter(UserInfo.user_name == "preetham").delete()
        self.session.commit()

        # User already exists
        mock_create_new_user.return_value = None
        res = self.app_client.post(url, json=data)
        assert res.status_code == 409

        users = (
            self.session.query(UserInfo).filter(UserInfo.user_name == "preetham").all()
        )
        assert len(users) == 0

    @mock.patch("flask_app.user_login")
    def test_login(self, mock_user_login):
        url = "/v1/auth/login"
        data = {"username": "preetham", "password": "password"}

        mock_user_login.return_value = {"access_token": "1", "refersh_token": "2"}
        res = self.app_client.post(url, json=data)
        assert res.status_code == 200

        mock_user_login.return_value = None
        res = self.app_client.post(url, json=data)
        assert res.status_code == 401

    @mock.patch("flask_app.user_logout")
    def test_logout(self, mock_user_logout):
        url = "/v1/auth/logout"

        # mock_user_login.return_value = {"access_token": "1", "refersh_token": "2"}
        res = self.app_client.post(url)
        assert res.status_code == 401

        # mock_user_login.return_value = None
        self.app_client.set_cookie("localhost", "refresh_token", "1")
        res = self.app_client.post(url)
        assert res.status_code == 200

        # Unset cookie by setting expires=0
        self.app_client.set_cookie("localhost", "refresh_token", "1", expires=0)

    @mock.patch("flask_app.check_userinfo")
    def test_auth_userinfo(self, mock_check_userinfo):
        url = "/v1/auth/userinfo"

        mock_check_userinfo.return_value = (
            {"access_token": "1", "refresh_token": "2"},
            {"username": "preetham"},
        )
        self.app_client.set_cookie("localhost", "access_token", "1")
        self.app_client.set_cookie("localhost", "refresh_token", "2")
        res = self.app_client.get(url)
        assert res.status_code == 200

        # Unset cookie by setting expires=0
        self.app_client.set_cookie("localhost", "access_token", "1", expires=0)
        self.app_client.set_cookie("localhost", "refresh_token", "2", expires=0)

        mock_check_userinfo.return_value = (dict(), None)
        self.app_client.set_cookie("localhost", "access_token", "1")
        self.app_client.set_cookie("localhost", "refresh_token", "2")
        res = self.app_client.get(url)
        assert res.status_code == 403

        # Unset cookie by setting expires=0
        self.app_client.set_cookie("localhost", "refresh_token", "1", expires=0)

    def test_create_userinfo(self):
        url = "/v1/users/create"

        ui = UserInfo(user_name=self.user_data["user_name"])
        session.add(ui)
        session.commit()

        res = self.app_client.post(url, json=self.user_data)

        assert res.status_code == 200

        users = (
            self.session.query(UserInfo).filter(UserInfo.user_name == "preetham").all()
        )
        assert len(users) == 1
        assert users[0].user_name == "preetham"
        assert users[0].first_name == "Preetham"
        assert users[0].last_name == "Maiya"
        assert users[0].mobile_number == "1234566789"
        assert users[0].email_id == "prma6536@colorado.edu"
        assert users[0].is_merchant == False
        assert users[0].created_by == "preetham"
        assert users[0].updated_by == "preetham"

        self.session.query(UserInfo).filter(UserInfo.user_name == "preetham").delete()
        self.session.commit()
