from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class UserPermission(Enum):
    ANONYMOUS = "ANONYMOUS"  # 비회원
    NORMAL = "NORMAL"  # 일반 회원
    ADMIN = "ADMIN"  # 관리자
    MASTER = "MASTER"  # 마스터

    def is_authenticated(self):
        return self in (self.NORMAL, self.ADMIN, self.MASTER)


@dataclass
class User:
    id: int | None
    email: str
    password: str
    permission: UserPermission
    is_active: bool
    last_login: datetime | None
    created_dtm: datetime
