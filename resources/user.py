import logging
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    get_jwt,
    jwt_required,
)
from passlib.hash import pbkdf2_sha256
from sqlalchemy import or_

from app_cache import AppCache
from db import db
from models import UserModel
from schemas import UserMeSchema, UserSchema, UserRegisterSchema, UserViewSchema
from services.utils import calculate_age_from_dob
from settings import REDIS_ENABLED

logger = logging.getLogger(__name__)
blp = Blueprint("Users", "users", description="Operations on users")

cache = AppCache().Cache()

@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserRegisterSchema)
    def post(self, user_data):
        if UserModel.query.filter(
            or_(
                UserModel.username == user_data["username"],
                UserModel.email == user_data["email"],
            )
        ).first():
            abort(409, message="A user with that username or email already exists.")

        user = UserModel(
            username=user_data["username"],
            email=user_data["email"],
            password=pbkdf2_sha256.hash(user_data["password"]),
        )
        db.session.add(user)
        db.session.commit()

        return {"message": "User created successfully."}, 201


@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel.query.filter(
            UserModel.username == user_data["username"]
        ).first()

        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {"access_token": access_token, "refresh_token": refresh_token}, 200

        abort(401, message="Invalid credentials.")


@blp.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        jti = get_jwt()["jti"]
        if REDIS_ENABLED:
            cache.set(jti, '0', timeout=3600*48)
        return {"access_token": new_token}, 200

@blp.route("/user")
class Me(MethodView):
    @jwt_required()
    @blp.response(200, UserMeSchema)
    def get(self):
        user_id = get_jwt_identity()
        redis_key =f'user_me_{user_id}'
        user = cache.get(redis_key) if REDIS_ENABLED else None
        if user:
            return user
        user = UserModel.query.get(user_id)
        if REDIS_ENABLED:
            cache.set(redis_key, user.serialize(), timeout=3600)
        return user

@blp.route("/user/<int:user_id>")
class User(MethodView):

    @blp.response(200, UserViewSchema)
    def get(self, user_id):
        redis_key =f'user_{user_id}'
        user = cache.get(redis_key) if REDIS_ENABLED else None
        if user:
            return user
        user = UserModel.query.get_or_404(user_id)
        user.profile.age = calculate_age_from_dob(user.profile.dob)
        if REDIS_ENABLED:
            cache.set(redis_key, user.serialize(), timeout=3600)
        return user

