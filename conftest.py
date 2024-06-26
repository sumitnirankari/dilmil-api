import os
import pytest
from flask_jwt_extended import create_access_token
from app import create_app
from db import db


@pytest.fixture(scope="session", autouse=True)
def set_env():
    os.environ["REDIS_ENABLED"] = "False"

@pytest.fixture()
def app():
    app = create_app("sqlite://")
    app.config.update(
        {
            "TESTING": True,
        }
    )
    with app.app_context():
        db.create_all()

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def fresh_jwt(app):
    with app.app_context():
        access_token = create_access_token(identity=1, fresh=True)
        return access_token


@pytest.fixture()
def jwt(app):
    with app.app_context():
        access_token = create_access_token(identity=1)
        return access_token


@pytest.fixture()
def admin_jwt(app):
    with app.app_context():
        access_token = create_access_token(
            identity=1, additional_claims={"is_admin": True}
        )
        return access_token
