from src import db
from src.models.model_base import ModelBase
from src.resources.utils import aes_decrypt


class FcmServerModel(ModelBase):
    __tablename__ = 'fcm_servers'
    uuid = db.Column(db.String(80), primary_key=True, nullable=False)
    key = db.Column(db.LargeBinary(), nullable=False)

    @classmethod
    def find_one(cls):
        return db.session.query(FcmServerModel).first()

    @classmethod
    def get_key(cls) -> str:
        fcm_server = db.session.query(FcmServerModel).first()
        if fcm_server:
            return aes_decrypt(fcm_server.key)
        return ''
