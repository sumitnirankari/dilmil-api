from db import db
from models.base_model import BaseModel

class UserModel(BaseModel):
    __tablename__ = "users"

    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String(256), unique=False, nullable=False)

    profile = db.relationship("UserProfileModel", uselist=False, back_populates='user', viewonly=True)
    preference = db.relationship("UserPrefModel", uselist=False, viewonly=True)

    def serialize(self):
        base_data = super().serialize()
        data = {
            'username': self.username,
            'email': self.email,
            'password': self.password,
            'profile': self.profile.serialize() if self.profile else None,
            'preference': self.preference.serialize() if self.preference else None
        }
        return {**base_data, **data}