import logging
from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_smorest import Blueprint

from app_cache import AppCache
from db import db
from dil_redis import DilRedis
from models import UserProfileModel
from schemas import ProfileSchema, ProfileViewSchema
from datetime import date

from services.utils import calculate_age_from_dob
from settings import REDIS_ENABLED

logger = logging.getLogger(__name__)
blp = Blueprint("UserProfile", "user_profile", description="Operations on user's profile")

cache = AppCache().Cache()

@blp.route("/profile")
class UserProfile(MethodView):
    @jwt_required()
    @blp.response(200, ProfileSchema)
    @blp.arguments(ProfileSchema)
    def post(self, profile_data):
        user_id = get_jwt_identity()
        profile = UserProfileModel.query.filter(UserProfileModel.user_id==user_id).first()
        # dob_format = '%Y-%m-%d'
        if profile is None:
            profile = UserProfileModel(
                user_id=user_id,
                first_name=profile_data['first_name'],
                last_name=profile_data['last_name'],
                dob=profile_data['dob'],
                height=profile_data['height'],
                # age = user_age
            )
            db.session.add(profile)
        else:
            profile.first_name=profile_data['first_name']
            profile.last_name=profile_data['last_name']
            profile.dob=profile_data['dob']
            profile.height=profile_data['height']
            # profile.age = user_age
        db.session.commit()
        if REDIS_ENABLED:
            cache.delete(f'user_{user_id}')
            cache.delete(f'profile_{profile.id}')
        return profile


@blp.route("/profile/<string:profile_id>")
class Profile(MethodView):

    @blp.response(200, ProfileViewSchema)
    def get(self, profile_id):
        redis_key =f'profile_{profile_id}'
        profile = cache.get(redis_key) if REDIS_ENABLED else None
        if profile:
            return profile
        profile = UserProfileModel.query.get_or_404(profile_id)
        profile.age = calculate_age_from_dob(profile.dob)
        if REDIS_ENABLED:
            cache.set(redis_key, profile.serialize(), timeout=3600)
        return profile
