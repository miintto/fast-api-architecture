from datetime import datetime

from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    DateTime,
    Enum,
    String,
)

from app.domain.user import User, UserPermission
from .base import Base


class UserEntity(Base[User]):
    __tablename__ = "tb_user"

    id = Column(BigInteger, primary_key=True)
    email = Column(String(200), comment="사용자 이메일", nullable=False, unique=True)
    password = Column(String(128), comment="비밀번호", nullable=True)
    permission = Column(
        Enum(UserPermission, native_enum=False, length=20),
        comment="주문 상태",
        nullable=False,
        default=UserPermission.NORMAL,
    )
    is_active = Column(Boolean, comment="활성화 여부", nullable=False, default=True)
    last_login = Column(
        DateTime(timezone=True), comment="주문 확정 일시", nullable=True
    )
    created_dtm = Column(
        DateTime, comment="생성 일시", nullable=False, default=datetime.utcnow
    )
