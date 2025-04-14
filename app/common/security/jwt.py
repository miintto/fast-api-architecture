from datetime import datetime, timedelta, timezone
import time

import jwt

from app.config.settings import get_settings
from app.domain.user import User

settings = get_settings()


class JWTProvider:
    JWT_EXPIRATION = timedelta(hours=12)
    JWT_SECRET_KEY = settings.SECRET_KEY
    ALGORITHM = "HS256"

    def encode(self, user: User) -> str:
        now = datetime.now(tz=timezone.utc)
        payload = {
            "pk": user.id,
            "email": user.email,
            "permission": user.permission.name,
            "exp": int(time.mktime((now + self.JWT_EXPIRATION).timetuple())),
            "iat": int(time.mktime(now.timetuple())),
        }
        return jwt.encode(
            payload=payload, key=self.JWT_SECRET_KEY, algorithm=self.ALGORITHM
        )

    def decode(self, token: str) -> dict:
        return jwt.decode(
            jwt=token, key=self.JWT_SECRET_KEY, algorithms=self.ALGORITHM
        )
