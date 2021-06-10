from sqlalchemy import UniqueConstraint

from src import db
from src.models.model_base import ModelBase


class UserSiteModel(ModelBase):
    __tablename__ = 'user_sites'
    uuid = db.Column(db.String(80), primary_key=True, nullable=False)
    user_uuid = db.Column(db.String, db.ForeignKey('users.uuid'), nullable=False)
    site_uuid = db.Column(db.String, db.ForeignKey('sites.uuid'), nullable=False)

    __table_args__ = (
        UniqueConstraint('user_uuid', 'site_uuid'),
    )

    @classmethod
    def find_by_user_uuid(cls, user_uuid: str):
        return cls.query.filter_by(user_uuid=user_uuid).all()
