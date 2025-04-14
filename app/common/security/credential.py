from pydantic import BaseModel

from app.adapter.outbound.persistence.entity.user import UserPermission


class CredentialPayload(BaseModel):
    pk: int
    email: str
    permission: UserPermission
    exp: int
    iat: int


class HTTPAuthorizationCredentials(BaseModel):
    scheme: str
    token: str
    payload: CredentialPayload
