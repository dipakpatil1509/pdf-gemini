from fastapi import APIRouter
from pdfGPT.views.PDF_GPT import get_reply, upload_file, get_messages

pdf_gpt_router = APIRouter()

pdf_gpt_router.add_api_route(
    "/upload_file",
    endpoint=upload_file,
    description="Upload file to chat",
    methods=["post"],
)

pdf_gpt_router.add_api_route(
    "/get_reply",
    endpoint=get_reply,
    description="Get reply to chat",
    methods=["post"],
)

pdf_gpt_router.add_api_route(
    "/get_messages",
    endpoint=get_messages,
    description="Get messages for the chat",
    methods=["get"],
)
