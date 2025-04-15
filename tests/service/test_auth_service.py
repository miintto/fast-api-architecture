from unittest.mock import MagicMock

from fastapi.exceptions import HTTPException
import pytest

from app.application.service.auth import AuthService
from .factory import UserFactory


@pytest.mark.asyncio
async def test_이미_가입한_이메일_에러(user_repo):
    mock_jwt = MagicMock()
    user_repo.find_by_email.return_value = UserFactory.generate()

    service = AuthService(mock_jwt, user_repo)
    with pytest.raises(HTTPException) as exc:
        await service.register("test@test.com", "password", "password")
    assert exc.value.status_code == 400


@pytest.mark.asyncio
async def test_회원가임_비밀번호_불일치_에러(user_repo):
    mock_jwt = MagicMock()
    user_repo.find_by_email.return_value = None

    service = AuthService(mock_jwt, user_repo)
    with pytest.raises(HTTPException) as exc:
        await service.register("test@test.com", "password", "pass")
    assert exc.value.status_code == 400


@pytest.mark.asyncio
async def test_회원가입_및_토큰_생성(user_repo):
    new_user = UserFactory.generate()
    mock_jwt = MagicMock()
    mock_jwt.encode.return_value = "auth-token"
    user_repo.find_by_email.return_value = None
    user_repo.save.return_value = new_user

    service = AuthService(mock_jwt, user_repo)
    token = await service.register("test@test.com", "password", "password")

    assert token == "auth-token"
    user_repo.save.assert_called_once()
    mock_jwt.encode.assert_called_once_with(new_user)


@pytest.mark.asyncio
async def test_존재하지_않는_이메일로_로그인(user_repo):
    mock_jwt = MagicMock()
    user_repo.find_by_email.return_value = None

    service = AuthService(mock_jwt, user_repo)
    with pytest.raises(HTTPException) as exc:
        await service.login("test@test.com", "password")
    assert exc.value.status_code == 400


@pytest.mark.asyncio
async def test_다른_비밀번호로_로그인(user_repo):
    mock_jwt = MagicMock()
    user_repo.find_by_email.return_value = UserFactory.generate(password="123")

    service = AuthService(mock_jwt, user_repo)
    with pytest.raises(HTTPException) as exc:
        await service.login("test@test.com", "password")
    assert exc.value.status_code == 400


@pytest.mark.asyncio
async def test_로그인_및_토큰_생성(user_repo):
    password = "qwe123!"
    user = UserFactory.generate(password=password)
    mock_jwt = MagicMock()
    mock_jwt.encode.return_value = "auth-token"
    user_repo.find_by_email.return_value = user
    user_repo.save.return_value = True

    service = AuthService(mock_jwt, user_repo)
    token = await service.login("test@test.com", password)

    assert token == "auth-token"
    user_repo.save.assert_called_once()
    mock_jwt.encode.assert_called_once_with(user)
