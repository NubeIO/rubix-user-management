import enum


class StateType(enum.Enum):
    VERIFIED = 'Verified'
    UNVERIFIED = 'Unverified'


class FcmDataType(enum.Enum):
    USER_VERIFICATION = 1
