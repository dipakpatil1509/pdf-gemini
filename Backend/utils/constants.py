from typing import Dict, Optional
from pydantic import BaseModel

class CustomException(Exception):
    def __init__(self, msg: str):
        self.msg = msg


class BaseResponse:
    success: bool = True
    message: str = ""
    data: Optional[Dict] = {}
    code: int = 200

    def __new__(
        cls,
        success: bool = True,
        message: str = "",
        data: dict = {},
        code: int = 200,
        **kwargs,
    ):
        if data is None:
            data = {}

        instance = {"success": success, "message": message, "data": data, "code": code}
        return instance


class GenericSuccessResponse(BaseModel):
    success: bool = True
    message: str = "Successfully completed!"
    data: dict = {}
    code: int = 200


class GenericErrorResponse(BaseModel):
    success: bool = False
    message: str = "Something went wrong!"
    data: dict = {}
    code: int = 400


class GenericInternalServerErrorResponse(BaseModel):
    success: bool = False
    message: str = "Something went wrong! Please try again or contact our support"
    data: dict = {}
    code: int = 500