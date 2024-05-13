from dataclasses import dataclass
from db import db
from models.base_model import BaseModel

@dataclass
class UserPrefModel(BaseModel):
    __tablename__ = "users_preferance"
    
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    height_min = db.Column(db.Integer, nullable=False)
    height_max = db.Column(db.Integer, nullable=False)
    age_min = db.Column(db.Integer, nullable=False)
    age_max = db.Column(db.Integer, nullable=False)

