from datetime import timedelta
import os, logging
from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from dotenv import load_dotenv

from app_cache import AppCache
from db import db

from settings import LOG_LEVEL, REDIS_ENABLED
from flask_caching import Cache

def create_app(db_url=None):
    app = Flask(__name__)
    load_dotenv()
    app.config["API_TITLE"] = "DilMil API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger"
    app.config["OPENAPI_SWAGGER_UI_CONFIG"] = {
        'deepLinking': True
    }
    app.config[
        "OPENAPI_SWAGGER_UI_URL"
    ] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv(
        "DATABASE_URL", "sqlite:///data.db"
    )
    # "postgresql://root:password@localhost:5432/dilmil"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["PROPAGATE_EXCEPTIONS"] = True

    db.init_app(app)
    migrate = Migrate(app, db)
    cache = AppCache(app).Cache()
    api = Api(app)

    app.config["JWT_SECRET_KEY"] = "sumit-dilmil-token"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=12)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=2)
    jwt = JWTManager(app)

    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        # TODO: Read from a config file instead of hard-coding
        if identity == 1:
            return {"is_admin": True}
        return {"is_admin": False}

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return (cache.get(jwt_payload["jti"]) != None) if REDIS_ENABLED else False

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "The token has expired.", "error": "token_expired"}),
            401,
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {"message": "Signature verification failed.", "error": "invalid_token"}
            ),
            401,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "description": "Request does not contain an access token.",
                    "error": "authorization_required",
                }
            ),
            401,
        )

    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {
                    "description": "The token is not fresh.",
                    "error": "fresh_token_required",
                }
            ),
            401,
        )

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {"description": "The token has been revoked.", "error": "token_revoked"}
            ),
            401,
        )

    from resources.user import blp as UserBlueprint
    from resources.user_profile import blp as ProfileBlueprint
    from resources.user_pref import blp as UserPrefBlueprint
    from resources.user_likes import blp as UserLikeBlueprint
    from resources.user_search import blp as UserSearchBlueprint
    api.register_blueprint(UserBlueprint)
    api.register_blueprint(ProfileBlueprint)
    api.register_blueprint(UserPrefBlueprint)
    api.register_blueprint(UserLikeBlueprint)
    api.register_blueprint(UserSearchBlueprint)
    
    logging.basicConfig(
        filename=os.getenv('SERVICE_LOG', 'server.log'),
        level=LOG_LEVEL,
        format='%(levelname)s: %(asctime)s pid:%(process)s module:%(module)s %(message)s',
        datefmt='%d/%m/%y %H:%M:%S',
    )

    return app

if __name__ == '__main__':
    server = create_app()
    server.run(host='0.0.0.0', port='5000')