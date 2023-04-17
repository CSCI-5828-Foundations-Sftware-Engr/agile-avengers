import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../"))

from config import user_management as config
from keycloak import KeycloakAdmin, KeycloakOpenID
from keycloak import KeycloakOpenIDConnection
import keycloak

CLIENT_SECRET_KEY = "Shhhh"
CLIENT_ID = "test"

keycloak_connection = KeycloakOpenIDConnection(
    server_url=config.keycloak_url,
    username="admin",
    password="admin",
    realm_name="master",
    client_id="admin-cli",
    verify=True,
)

keycloak_admin = KeycloakAdmin(
    server_url=config.keycloak_url, connection=keycloak_connection
)

client = keycloak_admin.create_client(
    skip_exists=True,
    payload={
        "clientId": CLIENT_ID,
        "clientAuthenticatorType": "client-secret",
        "secret": CLIENT_SECRET_KEY,
        "publicClient": False,
        "serviceAccountsEnabled": True,
        "authorizationServicesEnabled": True,
    },
)

keycloak_openid = KeycloakOpenID(
    server_url=config.keycloak_url,
    client_id="admin-cli",
    client_secret_key=CLIENT_SECRET_KEY,
    realm_name="master",
)


def create_new_user(username, password, email=None, first_name=None, last_name=None):
    try:
        new_user = keycloak_admin.create_user(
            {
                "email": email,
                "username": username,
                "enabled": True,
                "firstName": first_name,
                "lastName": last_name,
                "credentials": [
                    {
                        "value": password,
                        "type": "password",
                    }
                ],
            }
        )
        return new_user
    except keycloak.exceptions.KeycloakPostError as e:
        return None


def user_login(username, password):
    try:
        return keycloak_openid.token(username, password)
    except keycloak.exceptions.KeycloakAuthenticationError:
        return None


def user_logout(token):
    return keycloak_openid.logout(token)


def check_userinfo(token):
    try:
        return token, keycloak_openid.userinfo(token["access_token"])
    except keycloak.exceptions.KeycloakAuthenticationError:
        try:
            token = keycloak_openid.refresh_token(token["refresh_token"])
            return token, keycloak_openid.userinfo(token["access_token"])
        except keycloak.exceptions.KeycloakAuthenticationError:
            print("Unauthorized")
        except keycloak.exceptions.KeycloakPostError:
            print("no session exists")

    except keycloak.exceptions.KeycloakPostError:
        print("no session exists")

    return token, None
