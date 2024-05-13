from db import db
from models.base_model import BaseModel


class UserLikesModel(BaseModel):
    __tablename__ = "users_likes"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    target_user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    liked = db.Column(db.Boolean, nullable=True)
