from datetime import datetime, timezone
from db import db

class BaseModel(db.Model):
    __abstract__ = True
    
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now(tz=timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(tz=timezone.utc), onupdate=datetime.now(tz=timezone.utc))
    is_deleted = db.Column(db.Boolean, nullable=True)
    
    def serialize(self):
        return {
            'id': self.id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'is_deleted': self.is_deleted
        }