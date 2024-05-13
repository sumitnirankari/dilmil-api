import pytest
from flask import Flask
from flask_jwt_extended import create_access_token
from flask_smorest import Api
from flask_sqlalchemy import SQLAlchemy

from db import db
from models import UserPrefModel
from resources.user_pref import UserPreferences

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = "secret"
    app.config["TESTING"] = True

    db.init_app(app)
    with app.app_context():
        db.create_all()

    api = Api(app)
    api.register_blueprint(UserPreferences)

    yield app

    with app.app_context():
        db.drop_all()

def test_post_user_preference(app):
    with app.test_client() as client:
        # Create a test user
        access_token = create_access_token(identity="test_user")

        # Send a POST request to create a user preference
        response = client.post(
            "/preference",
            json={
                "preference_key": "theme",
                "preference_value": "dark"
            },
            headers={"Authorization": f"Bearer {access_token}"}
        )

        # Assert that the response status code is 200
        assert response.status_code == 200

        # Assert that the response JSON matches the expected user preference
        assert response.json == {
            "preference_key": "theme",
            "preference_value": "dark"
        }

        # Assert that the user preference is saved in the database
        with app.app_context():
            user_pref = UserPrefModel.query.filter_by(user_id="test_user").first()
            assert user_pref is not None
            assert user_pref.preference_key == "theme"
            assert user_pref.preference_value == "dark"
