import pytest
from flask import Flask
from flask_jwt_extended import create_access_token
from flask_smorest import Api
from flask_sqlalchemy import SQLAlchemy

from db import db
from models import UserProfileModel
from resources.user_profile import UserProfile, Profile
from schemas import ProfileSchema, ProfileViewSchema

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
        yield app

@pytest.fixture
def client(app):
    api = Api(app)
    api.register_blueprint(UserProfile)
    api.register_blueprint(Profile)
    return app.test_client()

def test_create_user_profile(client):
    access_token = create_access_token(identity="test_user")
    headers = {"Authorization": f"Bearer {access_token}"}
    data = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "dob": "1990-01-01"
    }
    response = client.post("/profile", json=data, headers=headers)
    assert response.status_code == 200
    assert response.json["name"] == "John Doe"
    assert response.json["email"] == "john.doe@example.com"

def test_get_user_profile(client):
    user_profile = UserProfileModel(name="John Doe", email="john.doe@example.com", dob="1990-01-01")
    db.session.add(user_profile)
    db.session.commit()
    response = client.get(f"/profile/{user_profile.id}")
    assert response.status_code == 200
    assert response.json["name"] == "John Doe"
    assert response.json["email"] == "john.doe@example.com"
