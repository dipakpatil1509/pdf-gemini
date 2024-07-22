from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from uvicorn import run as uvicorn_run
from views.routers import root_router
from fastapi.responses import JSONResponse
from fastapi.exceptions import FastAPIError, HTTPException, RequestValidationError
from utils.constants import (
    CustomException,
    BaseResponse,
    GenericSuccessResponse,
    GenericErrorResponse,
    GenericInternalServerErrorResponse,
)

local_hosts = ["localhost", "127.0.0.1", "0.0.0.0"]

app = FastAPI(
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
    title="PDF GPT API Docs",
)

origins = local_hosts

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=origins)


@app.exception_handler(Exception)
@app.exception_handler(FastAPIError)
@app.exception_handler(CustomException)
async def request_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=400, content=BaseResponse(False, str(exc), code=400)
    )


@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(
    request: Request, exc: RequestValidationError
):
    error_message = []
    for error in exc.errors():
        if error["loc"][0] == "body":
            error_message.append(f"{error['loc'][1]}-{error['msg']}".capitalize())
    return JSONResponse(
        status_code=400,
        content=BaseResponse(False, str(", ".join(error_message)), code=400),
    )


@app.exception_handler(404)
async def not_found_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=404,
        content=BaseResponse(
            False,
            "May be, you are lost in the eternity of pain and suffering!",
            code=404,
        ),
    )


@app.exception_handler(HTTPException)
@app.exception_handler(500)
async def internal_server_error_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content=BaseResponse(
            False,
            message="Something went wrong! Please try again or contact our support",
            code=500,
        ),
    )


app.include_router(
    root_router,
    responses={
        200: {"model": GenericSuccessResponse},
        400: {"model": GenericErrorResponse},
        422: {"model": GenericErrorResponse},
        500: {"model": GenericInternalServerErrorResponse},
    },
)

if __name__ == "__main__":
    uvicorn_run("main:app", host="0.0.0.0", port=8080, workers=4)
