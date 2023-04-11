PORT = 5000
HOST = "0.0.0.0"

api_version = "v1"

admin_username = "admin"
admin_password = "admin"

keycloak_domain = "localhost"
keycloak_url = f"http://{keycloak_domain}:8080"
keycloak_create_user = f"{keycloak_url}/auth/admin/realms/master/users"
keycloak_login_url = f"{keycloak_url}/auth/realms/master/protocol/openid-connect/token"
