from datetime import date, timedelta
import logging
from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_smorest import Blueprint
from sqlalchemy import and_

from app_cache import AppCache
from db import db
from models import UserProfileModel, UserModel
from models.user_like import UserLikesModel
from models.user_pref import UserPrefModel
from schemas import PaginationSchema, SearchPrefSchema, UsersListSchema, UsersProfileListSchema
from services.utils import calculate_age_from_dob
from settings import REDIS_ENABLED

logger = logging.getLogger(__name__)
blp = Blueprint("UserSearch", "user_search", description="Operations on user's search and recommendations")

cache = AppCache().Cache()

@blp.route("/search")
class UserSearch(MethodView):
    def serialize_search_result(self, result):
        return {
            "page": result.page,
            "pages": result.pages,
            "total": result.total,
            "per_page": result.per_page,
            "profiles": [p.serialize() for p in result.items]
        }
    # @cache.cached(timeout=3600)
    def search(self, user_id, age_min, age_max, height_min, height_max, search_data):
        redis_key = f"user_search_{user_id}_{age_min}_{age_max}_{height_min}_{height_max}_{search_data['show_liked']}_{search_data['sort_on']}_{search_data['page']}_{search_data['page_size']}"
        profiles = cache.get(redis_key) if REDIS_ENABLED else None
        if profiles:
            return profiles
        days_per_year = 365.24
        today = date.today()
        dob_max = today - timedelta(days=(age_min*days_per_year))
        dob_min = today - timedelta(days=(age_max*days_per_year))
        query = UserProfileModel.query.join(
                UserLikesModel, and_(UserLikesModel.user_id == user_id, UserLikesModel.target_user_id == UserProfileModel.user_id),  isouter=True
            ).filter(
            and_(height_min <= UserProfileModel.height, height_max >= UserProfileModel.height, 
                 dob_min <= UserProfileModel.dob, dob_max >= UserProfileModel.dob
            )
            )
        if not search_data['show_liked']:
            query = query.filter(UserLikesModel.liked == None)
        
        if search_data['sort_on']:
            field = getattr(UserProfileModel, search_data['sort_on'])
            query = query.order_by((field.desc() if search_data['sort_order'] == 'desc' else field.asc()))
        else:
            query = query.order_by(UserProfileModel.updated_at.asc())

        profiles = query.paginate(page=search_data['page'],per_page=search_data['page_size'],error_out=False)
        for profile in profiles.items:
            profile.age = calculate_age_from_dob(profile.dob)
        
        result = profiles
        if REDIS_ENABLED:
            result = self.serialize_search_result(profiles)
            cache.set(redis_key, result, timeout=3600)
        return result

    @jwt_required()
    @blp.response(200, UsersProfileListSchema)
    @blp.arguments(SearchPrefSchema)
    def post(self, search_data):
        user_id = get_jwt_identity()
        # pref = cache.get(f'user_pref_{user_id}') if redis.available() else None
        pref = cache.get(f'user_pref_{user_id}') if REDIS_ENABLED else None
        if pref is None:
            pref = UserPrefModel.query.filter(UserPrefModel.user_id==user_id).first()
            if pref:
                pref = pref.serialize()
                if REDIS_ENABLED:
                    cache.set(f'user_pref_{user_id}', pref)

        if pref is None:
            logger.debug(f'user_pref not available for user {user_id}')
            return {"message": "Please create your preference first"}, 412
        
        age_min, age_max, height_min, height_max = pref['age_min'], pref['age_max'], pref['height_min'], pref['height_max']
        return self.search(user_id, age_min, age_max, height_min, height_max, search_data)


@blp.route("/recommendations")
class UserRecommendations(MethodView):
    @jwt_required()
    @blp.response(200, UsersListSchema)
    @blp.arguments(PaginationSchema)
    def post(self, pagination):
        user_id = get_jwt_identity()
        users = UserModel.query.join(
            UserLikesModel, UserLikesModel.target_user_id == UserModel.id
            ).filter(
                and_(UserLikesModel.user_id==user_id, UserLikesModel.liked==None)
                ).order_by(
                    UserLikesModel.updated_at.desc()
                    ).paginate(page=pagination['page'],per_page=pagination['page_size'],error_out=False)
        for user in users.items:
            user.profile.age = calculate_age_from_dob(user.profile.dob)
        users.users = users.items
        return users
