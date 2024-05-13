import pytest
from flask import Flask
from flask_jwt_extended import create_access_token
from flask_smorest import Api
from flask_sqlalchemy import SQLAlchemy

from app_cache import AppCache
from db import db
from resources.user_search import UserSearch, UserRecommendations

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'secret'
    app.config['TESTING'] = True

    db.init_app(app)
    with app.app_context():
        db.create_all()

    yield app

@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client

def test_user_search(client):
    # Create a test user
    user_id = 1
    access_token = create_access_token(identity=user_id)

    # Make a search request
    response = client.post('/search', json={
        'search_data': {
            'show_liked': 'True',
            'sort_on': 'updated_at',
            'sort_order': 'desc',
            'page': 1,
            'page_size': 10
        }
    }, headers={'Authorization': f'Bearer {access_token}'})

    assert response.status_code == 200
    # Add more assertions here to validate the response data

def test_user_recommendations(client):
    # Create a test user
    user_id = 1
    access_token = create_access_token(identity=user_id)

    # Make a recommendations request
    response = client.post('/recommendations', json={
        'page': 1,
        'per_page': 10
    }, headers={'Authorization': f'Bearer {access_token}'})

    assert response.status_code == 200
    # Add more assertions here to validate the response data
