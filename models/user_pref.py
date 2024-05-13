from db import db
from models.base_model import BaseModel

class UserPrefModel(BaseModel):
    __tablename__ = "users_preferance"
    
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    height_min = db.Column(db.Integer, nullable=False)
    height_max = db.Column(db.Integer, nullable=False)
    age_min = db.Column(db.Integer, nullable=False)
    age_max = db.Column(db.Integer, nullable=False)
    
    def serialize(self):
        base_dict = super().serialize()
        user_pref_dict = {
            "user_id": self.user_id,
            "height_min": self.height_min,
            "height_max": self.height_max,
            "age_min": self.age_min,
            "age_max": self.age_max
        }
        return {**base_dict, **user_pref_dict}
