# config.py
import os


class BaseConfig(object):
    SECRET_KEY = os.environ['SECRET_KEY']
    DEBUG = os.environ['DEBUG']
    POSTGRES_DB = os.environ['POSTGRES_DB']
    POSTGRES_USER = os.environ['POSTGRES_USER']
    POSTGRES_PASSWORD = os.environ['POSTGRES_PASSWORD']
    DB_SERVICE = os.environ['DB_SERVICE']
    DB_PORT = os.environ['DB_PORT']
    SQLALCHEMY_DATABASE_URI = 'postgresql://{0}:{1}@{2}:{3}/{4}'.format(
        POSTGRES_USER, POSTGRES_PASSWORD, DB_SERVICE, DB_PORT, POSTGRES_DB
    )

    OIDC_CLIENT_SECRETS = "client_secrets.json"
    OIDC_COOKIE_SECURE = False
    OIDC_CALLBACK_ROUTE = "/authorization-code/callback"
    OIDC_SCOPES = ["openid", "email", "profile", "groups"]
    # SECRET_KEY"] = "{{ LONG_RANDOM_STRING }}"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    TEMPLATES_AUTO_RELOAD = True

    okta_org_url = "https://dev-851814.okta.com"
    okta_auth_token = "00vhnNlDXaOhDUWn-DicSoQCsTOdieLrfIfLaJPK-9"