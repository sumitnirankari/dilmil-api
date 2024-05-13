import pytest
from flask import Flask
from flask_jwt_extended import create_access_token
from flask_smorest import Api
from flask_sqlalchemy import SQLAlchemy

from resources.user_likes import UserLikes, UserLiked

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = "secret"
    app.config["TESTING"] = True

    with app.app_context():
        db = SQLAlchemy(app)
        api = Api(app)
        api.register_blueprint(UserLikes.blp)
        api.register_blueprint(UserLiked.blp)

        db.create_all()

        yield app

@pytest.fixture
def client(app):
    return app.test_client()

def test_post_user_likes(client):
    access_token = create_access_token(identity="test_user")

    response = client.post(
        "/likes",
        json={
            "user_id": 1,
            "liked_user_id": 2
        },
        headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 200
    assert response.json == {
        "user_id": 1,
        "liked_user_id": 2
    }

def test_get_user_liked(client):
    access_token = create_access_token(identity="test_user")

    response = client.get(
        "/liked/1/1/20",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 200
    assert response.json == {
        "users": [],
        "page": 1,
        "page_size": 20
    }
