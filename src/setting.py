import json
import os
import secrets

from flask import Flask

from src.utils.file import read_file, write_file


class BaseSetting:

    def reload(self, setting: dict):
        if setting is not None:
            self.__dict__ = {k: setting.get(k, v) for k, v in self.__dict__.items()}
        return self

    def serialize(self, pretty=True) -> str:
        return json.dumps(self, default=lambda o: o.__dict__, indent=2 if pretty else None)

    def to_dict(self):
        return json.loads(self.serialize(pretty=False))


class AppSetting:
    PORT: int = 1617
    GLOBAL_DIR_ENV = 'APP_BASE_GLOBAL'
    DATA_DIR_ENV = 'APP_BASE_DATA'
    CONFIG_DIR_ENV = 'APP_BASE_CONFIG'
    FLASK_KEY: str = 'APP_SETTING'
    default_global_dir = 'out'
    default_data_dir: str = 'data'
    default_config_dir: str = 'config'
    default_setting_file: str = 'config.json'
    default_logging_conf: str = 'logging.conf'
    fallback_logging_conf: str = 'config/logging.conf'
    fallback_prod_logging_conf: str = 'config/logging.prod.conf'
    default_secret_key_file = 'secret_key.txt'
    default_fcm_secret_key_file = 'fcm_secret_key.txt'
    default_fcm_url = 'https://fcm.googleapis.com/fcm/send'

    def __init__(self, **kwargs):
        self.__port = kwargs.get('port') or AppSetting.PORT
        self.__global_dir = self.__compute_dir(kwargs.get('global_dir'), AppSetting.default_global_dir, 0o777)
        self.__data_dir = self.__compute_dir(self.__join_global_dir(kwargs.get('data_dir')),
                                             self.__join_global_dir(AppSetting.default_data_dir))
        self.__config_dir = self.__compute_dir(self.__join_global_dir(kwargs.get('config_dir')),
                                               self.__join_global_dir(AppSetting.default_config_dir))
        self.__prod = kwargs.get('prod') or False
        self.__secret_key = ''
        self.__secret_key_file = os.path.join(self.__config_dir, self.default_secret_key_file)
        self.__fcm_secret_key = ''
        self.__fcm_secret_key_file = os.path.join(self.__config_dir, self.default_fcm_secret_key_file)

    @property
    def port(self):
        return self.__port

    @property
    def global_dir(self):
        return self.__global_dir

    @property
    def data_dir(self):
        return self.__data_dir

    @property
    def config_dir(self):
        return self.__config_dir

    @property
    def prod(self) -> bool:
        return self.__prod

    @property
    def secret_key(self) -> str:
        return self.__secret_key

    @property
    def fcm_secret_key(self) -> str:
        return self.__fcm_secret_key

    def serialize(self, pretty=True) -> str:
        m = {
            'prod': self.prod, 'global_dir': self.global_dir, 'data_dir': self.data_dir, 'config_dir': self.config_dir
        }
        return json.dumps(m, default=lambda o: o.to_dict() if isinstance(o, BaseSetting) else o.__dict__,
                          indent=2 if pretty else None)

    def reload(self, setting_file: str):
        return self

    def init_app(self, app: Flask):
        self.__secret_key = AppSetting.__handle_secret_key(self.__secret_key_file)
        self.__fcm_secret_key = AppSetting.__handle_fcm_secret_key(self.__fcm_secret_key_file)
        app.config[AppSetting.FLASK_KEY] = self
        return self

    def __join_global_dir(self, _dir):
        return _dir if _dir is None or _dir.strip() == '' else os.path.join(self.__global_dir, _dir)

    @staticmethod
    def __compute_dir(_dir: str, _def: str, mode=0o744) -> str:
        d = os.path.join(os.getcwd(), _def) if _dir is None or _dir.strip() == '' else _dir
        d = d if os.path.isabs(d) else os.path.join(os.getcwd(), d)
        os.makedirs(d, mode, True)
        return d

    @staticmethod
    def __handle_secret_key(secret_key_file) -> str:
        existing_secret_key = read_file(secret_key_file)
        if existing_secret_key.strip():
            return existing_secret_key

        secret_key = AppSetting.__create_secret_key(24)
        write_file(secret_key_file, secret_key)
        return secret_key

    @staticmethod
    def __handle_fcm_secret_key(fcm_secret_key_file) -> str:
        existing_secret_key = read_file(fcm_secret_key_file)
        if existing_secret_key.strip():
            return existing_secret_key

        secret_key = f'{AppSetting.__create_secret_key(8)}:{AppSetting.__create_secret_key(16)}'
        write_file(fcm_secret_key_file, secret_key)
        return secret_key

    @staticmethod
    def __create_secret_key(_bytes: int):
        return secrets.token_hex(_bytes)
