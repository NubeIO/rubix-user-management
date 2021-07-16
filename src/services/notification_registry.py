import datetime
import logging
from typing import Dict, Union

import gevent

from src.setting import NotificationSetting
from src.utils.singleton import Singleton

logger = logging.getLogger(__name__)


class NotificationRegistry(metaclass=Singleton):
    """
        Notification format
        {
          "<key1>": "<current_timestamp>",
          "<key2>": "<current_timestamp>"
        }
    """

    def __init__(self):
        self.__config: Union[NotificationSetting, None] = None
        self.__notifications: Dict[str, datetime.datetime] = {}

    @property
    def config(self) -> Union[NotificationSetting, None]:
        return self.__config

    @property
    def notifications(self) -> Dict[str, datetime.datetime]:
        return self.__notifications

    def register(self, config: NotificationSetting):
        logger.info(f"Called notification registration")
        self.__config = config
        while True:
            self.__check_and_clear_notification()
            gevent.sleep(self.config.timer * 60)

    def check_and_add_notification(self, key: str) -> bool:
        notification = self.__notifications.get(key, None)
        if notification is None:
            self.__notifications[key] = datetime.datetime.utcnow()
            return True
        return False

    def __check_and_clear_notification(self):
        self.__notifications = {k: v for k, v in self.__notifications.items() if
                                (datetime.datetime.utcnow() - v).total_seconds() <= (self.config.resend * 60)}
