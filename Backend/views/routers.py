from fastapi import APIRouter
from pdfGPT.router.router import pdf_gpt_router
from utils.constants import BaseResponse

root_router = APIRouter()

@root_router.get("/", tags=["Health Check"])
async def main():
    return BaseResponse(
        message="Dekho ye chal raha hai... Miracle, Miracle, Miracle!!!"
    )


root_router.include_router(pdf_gpt_router, tags=["PDF GPT"])