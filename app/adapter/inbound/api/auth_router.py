from fastapi import APIRouter, Depends

from app.application.port.input.auth_usecase import AuthUseCase
from app.application.service.auth_service import AuthService
from app.common.response import JSONResponse
from .schemas.auth import LoginInfo, RegisterInfo

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", summary="회원가입")
async def register(
    body: RegisterInfo,
    service: AuthUseCase = Depends(AuthService),
) -> JSONResponse:
    token = await service.register(**body.model_dump())
    return JSONResponse(content={"token": token}, status_code=200)


@router.post("/login", summary="로그인")
async def login(
    body: LoginInfo,
    service: AuthUseCase = Depends(AuthService),
) -> JSONResponse:
    token = await service.login(**body.model_dump())
    return JSONResponse(content={"token": token}, status_code=200)
