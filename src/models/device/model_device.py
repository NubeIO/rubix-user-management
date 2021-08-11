from sqlalchemy import UniqueConstraint

from src import db
from src.models.enum import Platform
from src.models.model_base import ModelBase
from src.utils.notification import send_fcm_notification


class DeviceModel(ModelBase):
    __tablename__ = 'devices'
    uuid = db.Column(db.String(80), primary_key=True, nullable=False)
    user_uuid = db.Column(db.String, db.ForeignKey('users.uuid'), nullable=False)
    device_id = db.Column(db.String(80), nullable=True)
    platform = db.Column(db.Enum(Platform), nullable=False, default=Platform.ANDROID)

    __table_args__ = (
        UniqueConstraint('user_uuid', 'device_id'),
    )

    @classmethod
    def find_by_user_uuid_and_uuid(cls, user_uuid: str, uuid: str):
        return cls.query.filter_by(user_uuid=user_uuid, uuid=uuid).first()

    @classmethod
    def find_by_device_id(cls, device_id: str):
        return cls.query.filter_by(device_id=device_id).first()

    @classmethod
    def find_by_user_uuid_and_device_id(cls, user_uuid: str, device_id):
        return cls.query.filter_by(user_uuid=user_uuid, device_id=device_id).first()

    @classmethod
    def find_all_by_user_uuid(cls, user_uuid: str):
        return cls.query.filter_by(user_uuid=user_uuid).all()

    @classmethod
    def send_notification_by_user_uuid(cls, user_uuid: str, key: str, data: dict):
        devices = cls.find_all_by_user_uuid(user_uuid)
        for device in devices:
            if 'to' in data:
                data['to'] = device.device_id
            content = send_fcm_notification(key, data)
            failure: bool = bool(content.get('failure', False))
            results = content.get('results', [])
            if failure and len(results) > 0 and (
                    results[0].get('error') == 'InvalidRegistration' or results[0].get('error') == 'NotRegistered'):
                device.delete_from_db()
