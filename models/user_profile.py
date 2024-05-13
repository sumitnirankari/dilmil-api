from db import db
from models.base_model import BaseModel


class UserProfileModel(BaseModel):
    __tablename__ = "users_profiles"

    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    height = db.Column(db.Integer, nullable=False)
    dob = db.Column(db.Date, nullable=False)
    # age = db.Column(db.Integer, nullable=False)

    user = db.relationship("UserModel",  uselist=False, back_populates='profile', viewonly=True)
