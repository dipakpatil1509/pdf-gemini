import json
import os
import shutil
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Union, List, Tuple
import google.generativeai as genai
import joblib
import litellm
from fastapi import UploadFile
from google.generativeai.types.content_types import ContentDict

from models.database import Database
from models.models import ChatMessages, PDFText
from utils.constants import CustomException
from utils.env_vars import get_env_var

from .process_pdf import ProcessPDF
from .semantic_search import SemanticSearch

litellm.set_verbose = True

TEMP_PATH = os.path.join(Path(__file__).parent.parent, "temp")
TEMP_PDF_PATH = os.path.join(TEMP_PATH, "pdf")
os.makedirs(TEMP_PDF_PATH, exist_ok=True)
TEMP_MODEL_PATH = os.path.join(TEMP_PATH, "semantic_search")
os.makedirs(TEMP_MODEL_PATH, exist_ok=True)
TEMP_MODEL_FILE_PATH = os.path.join(TEMP_MODEL_PATH, "semantic_search_{id}.sav")

GPT_ENGINE = "gemini-1.5-flash-latest"

GEMINI_API_KEY = get_env_var("GEMINI_API_KEY")

genai.configure(api_key=str(GEMINI_API_KEY))

model = genai.GenerativeModel(GPT_ENGINE)

CONTEXT_QUERY = """
    Instructions: Compose a comprehensive reply to the query using the provided text segments,
    which are associated with page numbers. Cite each reference using [Page Number: #] notation,
    where # is the page number provided with each text segment. Ensure citations are placed at the
    end of each relevant sentence. If the text mentions multiple subjects with the same name,
    create distinct answers for each. Use only the information found in the text segments and
    do not include any additional information. Make sure the response is correct and does not
    contain false information. If the text does not address the query, state 'Text Not Found in PDF'.
    Ignore irrelevant text segments that do not pertain to the question. Answer only what is asked.
    The answer should be concise and straightforward. Provide step-by-step explanations if necessary.
    If the PDF description is available, begin the response with a general statement summarizing the document's content.
    PDF Description: {pdf_description}
""".replace(
    "\n", " "
)


class PDF_GPT:
    def __init__(self) -> None:
        pass
    
    def get_pdf_text(self, pdf_chat_id: int)-> PDFText:
        db = Database()
        with db.get_session() as session:
            pdf_chat = session.query(PDFText).get(pdf_chat_id)
            if pdf_chat == None:
                raise CustomException("PDF is not uploaded")

            return pdf_chat
        
    def create_and_get_semantic_search(
        self, pdf_chat_id: int, processed_text: Union[List[dict], None] = None
    ) -> SemanticSearch:

        file_path = TEMP_MODEL_FILE_PATH.format(id=pdf_chat_id)
        print("Reading", file_path, os.path.exists(file_path))
        if os.path.exists(file_path):
            print("Using previous Semantic Search")
            semantic_search: SemanticSearch = joblib.load(file_path)
            return semantic_search

        if processed_text == None:
            pdf_chat = self.get_pdf_text(pdf_chat_id)
            processed_text = pdf_chat.processed_text

        semantic_search = SemanticSearch()
        semantic_search.fit([json.dumps(page) for page in processed_text])

        joblib.dump(semantic_search, file_path)

        return semantic_search

    def pdf_process(self, file: UploadFile, pdf_description: str) -> PDFText:

        suffix = Path(file.filename).suffix
        with NamedTemporaryFile(suffix=suffix, dir=TEMP_PDF_PATH, delete=False) as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmp_path = Path(tmp.name)

        pdf_processed = ProcessPDF()

        pdf_chat, processed_text = pdf_processed.read_and_save_pdf(
            tmp_path, pdf_description
        )

        self.create_and_get_semantic_search(pdf_chat.id, processed_text)

        return pdf_chat

    def get_llm_response(self, messages: list[dict]):
        try:
            history = []
            for msg in messages:
                role = msg["role"]
                history.append(ContentDict(parts=msg["content"], role=role))
            last_message = history.pop()
            chat = model.start_chat(history=history)
            response = chat.send_message(last_message)
            message = response.candidates[0].content.parts[0].text
        except Exception as e:
            raise CustomException(f"API Error: {str(e)}")

        return message
    
    def get_messages(self, pdf_chat_id:int) -> List[ChatMessages]:
        # OLD MESSAGES
        old_messages: List[ChatMessages] = []

        db = Database()
        with db.get_session() as session:
            pdf_chat_messages = (
                session.query(ChatMessages)
                .filter(
                    ChatMessages.pdf_text_id == pdf_chat_id,
                    ChatMessages.status == ChatMessages.STATUS.ACTIVE,
                )
                .order_by(ChatMessages.created_at.asc())
                .values(ChatMessages.message, ChatMessages.message_type)
            )

            for message_instance in pdf_chat_messages:
                message, role = message_instance
                role = role.name.lower()
                if role == "system":
                    role = "model"
                old_messages.append({"role": role, "content": message})
    
        return old_messages

    def generate_answer(self, question: str, pdf_chat_id: int):

        pdf_chat = self.get_pdf_text(pdf_chat_id)
        semantic_search = self.create_and_get_semantic_search(pdf_chat_id)

        topn_chunks = semantic_search.get_text(question)

        prompt = ""
        prompt += "search results:\n\n"
        for c in topn_chunks:
            prompt += c + "\n\n"

        prompt += f"{CONTEXT_QUERY.format(pdf_description=pdf_chat.context)}\n\nQuestion: {question}\nAnswer:"

        old_messages = self.get_messages(pdf_chat_id)

        messages = old_messages + [
            {"content": prompt, "role": "user"},
        ]

        answer = self.get_llm_response(messages)

        db = Database()
        with db.get_session() as session:
            new_messages = [
                ChatMessages(
                    message=question,
                    message_type=ChatMessages.MESSAGE_TYPE.USER,
                    pdf_text_id=pdf_chat_id,
                ),
                ChatMessages(
                    message=answer,
                    message_type=ChatMessages.MESSAGE_TYPE.SYSTEM,
                    pdf_text_id=pdf_chat_id,
                ),
            ]
            session.add_all(new_messages)
            session.commit()

        return answer
