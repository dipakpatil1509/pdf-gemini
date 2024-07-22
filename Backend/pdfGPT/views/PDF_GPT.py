from fastapi import UploadFile
from pydantic import BaseModel, Field

from utils.constants import BaseResponse
from pdfGPT.utils.pdf_gpt import PDF_GPT


async def upload_file(file: UploadFile, pdf_description: str = None):
    pdf_gpt = PDF_GPT()
    pdf_chat = pdf_gpt.pdf_process(file, pdf_description)

    data = {"pdf_chat_id": pdf_chat.id}

    return BaseResponse(success=True, message="Successfully uploaded file", data=data)


class GetReplyReqBody(BaseModel):
    text_input: str = Field(max_length=3000, min_length=1)
    pdf_id: int


async def get_reply(request_body: GetReplyReqBody):
    pdf_gpt = PDF_GPT()

    data = {"pdf_chat_id": request_body.pdf_id}

    answer = pdf_gpt.generate_answer(request_body.text_input, request_body.pdf_id)

    data["answer"] = answer

    return BaseResponse(success=True, message="Successfully got the answer", data=data)


async def get_messages(pdf_id: int):
    pdf_gpt = PDF_GPT()

    old_messages = pdf_gpt.get_messages(pdf_id)

    return BaseResponse(success=True, message="Successfully got the messages", data=old_messages)
