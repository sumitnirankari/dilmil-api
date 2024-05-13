import logging
from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_smorest import Blueprint
from rq import Queue
from sqlalchemy import and_

from db import db
from dil_redis import DilRedis
from models import UserModel
from models.user_like import UserLikesModel
from schemas import UserLikesSchema, UsersListSchema
from settings import REDIS_HOST, REDIS_PORT
from tasks import send_match_notification_to_users

logger = logging.getLogger(__name__)
blp = Blueprint("UserLikes", "user_likes", description="Operations on user's likes")
redis = DilRedis()
redis_client = redis.redis_client()
queue = Queue("emails", connection=redis_client)

@blp.route("/likes")
class UserLikes(MethodView):
    @jwt_required()
    @blp.response(200, UserLikesSchema)
    @blp.arguments(UserLikesSchema)
    def post(self, like_data):
        user_id = get_jwt_identity()
        like = UserLikesModel.query.filter(UserLikesModel.user_id==user_id and UserLikesModel.target_user_id==like_data['target_user_id']).first()
        # dob_format = '%Y-%m-%d'
        if like is None:
            like = UserLikesModel(
                user_id=user_id,
                target_user_id=like_data['target_user_id'],
                liked=like_data['liked'],
            )
            db.session.add(like)
        else:
            like.liked=like_data['liked']
        self.check_for_match(like)
        db.session.commit()
        return like

    def check_for_match(self, like: UserLikesModel):
        if like.liked:
            reverse_like = UserLikesModel.query.filter(UserLikesModel.user_id==like.target_user_id and UserLikesModel.target_user_id==like.user_id).first()
            if reverse_like:
                logger.debug(f'Its a match between user {like.user_id} and {like.target_user_id}')
                if redis.available():
                    queue.enqueue(send_match_notification_to_users, UserModel.query.get(like.user_id), UserModel.query.get(reverse_like.user_id))

@blp.route("/liked/<int:liked>/<int:page>/<int:page_size>", defaults={"page": 1, "page_size": 20})
class UserLiked(MethodView):
    @jwt_required()
    @blp.response(200, UsersListSchema)
    def get(self, liked, page, page_size):
        user_id = get_jwt_identity()
        users = UserModel.query.join(UserLikesModel, UserLikesModel.target_user_id == UserModel.id).filter(and_(UserLikesModel.user_id==user_id, UserLikesModel.liked==liked)).order_by(UserLikesModel.updated_at.desc()).paginate(page=page,per_page=page_size,error_out=False)
        users.users = users.items
        return users
