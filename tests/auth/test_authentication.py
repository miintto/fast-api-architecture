from unittest.mock import MagicMock, patch

from fastapi import HTTPException
import pytest
from starlette.datastructures import Headers

from app.common.authentication import Authentication
from app.common.security.credential import HTTPAuthorizationCredentials


@pytest.mark.asyncio
async def test_헤더에_키값이_없는_경우():
    mock_request = MagicMock()
    mock_request.headers = Headers(scope={"headers": []})

    auth = Authentication()
    with pytest.raises(HTTPException) as exc:
        await auth(request=mock_request)
    assert exc.value.status_code == 401


@pytest.mark.asyncio
async def test_잘못된_형식의_토큰():
    token = "token"
    mock_request = MagicMock()
    mock_request.headers = Headers(scope={"headers": [(b"authorization", token.encode())]})

    auth = Authentication()
    with pytest.raises(HTTPException) as exc:
        await auth(request=mock_request)
    assert exc.value.status_code == 401


@pytest.mark.asyncio
async def test_토큰_디코딩_실패():
    token = "JWT token"
    mock_request = MagicMock()
    mock_request.headers = Headers(scope={"headers": [(b"authorization", token.encode())]})

    auth = Authentication()
    with pytest.raises(HTTPException) as exc:
        await auth(request=mock_request)
    assert exc.value.status_code == 401


@pytest.mark.asyncio
@patch("app.common.security.jwt.JWTProvider.decode", return_value={})
async def test_잘못된_정보를_담은_토큰(mock_decode):
    token = "JWT token"
    mock_request = MagicMock()
    mock_request.headers = Headers(scope={"headers": [(b"authorization", token.encode())]})

    auth = Authentication()
    with pytest.raises(HTTPException) as exc:
        await auth(request=mock_request)
    assert exc.value.status_code == 401
    mock_decode.assert_called_once()


@pytest.mark.asyncio
@patch(
    "app.common.security.jwt.JWTProvider.decode",
    return_value={"pk": 1, "email": "test@test.com", "permission": "NORMAL", "exp": -1, "iat": -1},
)
async def test_토큰_성공(mock_decode):
    token = "JWT token"
    mock_request = MagicMock()
    mock_request.headers = Headers(scope={"headers": [(b"authorization", token.encode())]})

    auth = Authentication()
    credential = await auth(request=mock_request)

    assert isinstance(credential, HTTPAuthorizationCredentials)
    mock_decode.assert_called_once()
