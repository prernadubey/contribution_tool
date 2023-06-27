import typing as t

from fastapi import APIRouter, Depends, Header
from fastapi.responses import JSONResponse

from components.application.get_current_user import GetCurrentUser
from components.application.uc_response import UseCaseResponseStatus
from components.controller.fastapi.dependencies import get_users_repository
from components.controller.fastapi.error_processor import (
    process_controller_error_usecase_response,
)
from components.controller.fastapi.routers.v1.schemas import (
    BaseRequestsResponse,
    UserSchema,
)
from components.domain.user import User

USER_ID = "X-User-ID"

JSON_RESPONSE = {
    "title": "Authorization Error",
    "status": 401,
    "detail": f"Unauthorized error occurred. Verify {USER_ID} header",
}

router = APIRouter(tags=["Current User"])


class UserResponse(UserSchema, BaseRequestsResponse):
    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "ID": "4060000000000000000",
                "name": "John",
                "surname": "Smith",
                "email": "john_smith@epam.com",
                "role": "user",
            }
        }


@router.get("/users/me", response_model=t.Optional[UserResponse])
async def get_current_user(
    users_repo=Depends(get_users_repository),
    user_id: int = Header(None, alias=USER_ID),
):
    if not user_id:
        return JSONResponse(content=JSON_RESPONSE, status_code=401)

    usecase = GetCurrentUser(users_repo)
    uc_request = usecase.Request(data={"user_id": user_id})
    uc_response = await usecase.execute(request=uc_request)
    if uc_response.status is not UseCaseResponseStatus.SUCCESS or not uc_response.data:
        return process_controller_error_usecase_response(use_case_response=uc_response)

    response_data: User = uc_response.data

    return UserResponse(
        ID=response_data.id,
        name=response_data.name,
        surname=response_data.surname,
        email=response_data.email,
        role=response_data.role,
    )
