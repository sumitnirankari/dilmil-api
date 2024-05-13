from db import db
from models.base_model import BaseModel

class UserProfileModel(BaseModel):
    __tablename__ = "users_profiles"

    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    height = db.Column(db.Integer, nullable=False)
    dob = db.Column(db.Date, nullable=False)

    user = db.relationship("UserModel", uselist=False, back_populates='profile', viewonly=True)

    def serialize(self):
        base_data = super().serialize()
        data = {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'user_id': self.user_id,
            'height': self.height,
            'dob': self.dob
        }
        return {**base_data, **data}
