from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from schemas import APIResponseSchema, NewUserSchema
from utils.DataBaseManager import DB
from utils.security import getCurrentUserAuthenticated

router = APIRouter(prefix="/user", tags=["user"])

T_CurrentUser = Annotated[str, Depends(getCurrentUserAuthenticated)]


# Create new user
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=APIResponseSchema,
)
def handleNewUser(user: NewUserSchema):
    db_response = DB.createNewUser(user)
    if db_response.data_type == "error":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=db_response.message
        )
    return db_response


@router.get(
    "/{user_id}",
    response_model=APIResponseSchema,
)
async def getUserDataById(
    user_id: int,
):
    db_response = DB.getUserDataById(user_id)
    if db_response.data_type == "error":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=db_response.message
        )
    return db_response


@router.put(
    "/{user_id}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=APIResponseSchema,
)
def updateUserData(
    user_id: int,
    user_new_data: NewUserSchema,
    current_user_authenticated: T_CurrentUser,
):
    __user = DB.getUserDataById(user_id)
    if current_user_authenticated != __user.user_data.get("username"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=(
                "You must have admin previlegies to change other user's data"
            ),
        )
    db_response = DB.updateUser(user_id, user_new_data)
    return db_response
