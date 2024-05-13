import logging
from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_smorest import Blueprint

from app_cache import AppCache
from db import db
from models import UserPrefModel
from schemas import UserPrefSchema
from settings import REDIS_ENABLED

logger = logging.getLogger(__name__)
blp = Blueprint("UserPreferences", "user_pref", description="Operations on user's preferences")

cache = AppCache().Cache()

@blp.route("/preference")
class UserPreferences(MethodView):
    @jwt_required()
    @blp.response(200, UserPrefSchema)
    @blp.arguments(UserPrefSchema)
    def post(self, user_pref):
        user_id = get_jwt_identity()
        pref = UserPrefModel.query.filter(UserPrefModel.user_id==user_id).first()
        # dob_format = '%Y-%m-%d'
        if pref is None:
            pref = UserPrefModel(
                user_id=user_id,
                age_min=user_pref['age_min'],
                age_max=user_pref['age_max'],
                height_min=user_pref['height_min'],
                height_max=user_pref['height_max'],
            )
            db.session.add(pref)
        else:
            pref.age_min=user_pref['age_min']
            pref.age_max=user_pref['age_max']
            pref.height_min=user_pref['height_min']
            pref.height_max=user_pref['height_max']
        db.session.commit()
        if REDIS_ENABLED:
            cache.delete(f'user_pref_{user_id}')
        return pref
