import re
from typing import Dict, List, Tuple

import fitz

# import nltk
# from nltk.corpus import stopwords
# from nltk.stem import WordNetLemmatizer
# from nltk.tokenize import word_tokenize

from models.database import Database
from models.models import PDFText

# nltk.download("punkt")
# nltk.download("stopwords")
# nltk.download("wordnet")


class ProcessPDF:

    def read_and_save_pdf(
        self, pdf_path: str, pdf_description: str
    ) -> Tuple[PDFText, List[Dict[str, str]]]:
        doc = fitz.open(pdf_path)
        total_pages = doc.page_count

        text_by_page = []
        cleaned_text_by_page = []

        for i in range(total_pages):
            text = doc.load_page(i).get_text("text")
            cleaned_text = self.preprocess_text(text)
            text_by_page.append({"page_number": i + 1, "text": text})
            cleaned_text_by_page.append(
                {"page_number": i + 1, "processed_text": cleaned_text}
            )

        doc.close()

        db = Database()
        with db.get_session() as session:
            pdfChat = PDFText(
                text=text_by_page,
                processed_text=cleaned_text_by_page,
                context=pdf_description,
            )

            session.add(pdfChat)
            session.commit()

            session.refresh(pdfChat)

        return pdfChat, cleaned_text_by_page

    def preprocess_text(self, text: str) -> str:
        text = text.replace("\n", " ")
        text = re.sub(r"\s+", " ", text)
        text = re.sub(r"\W+", " ", text)

        return text

        # tokens = word_tokenize(text.lower())
        # tokens = [word for word in tokens if word.isalnum()]
        # stop_words = set(stopwords.words('english'))
        # tokens = [word for word in tokens if word not in stop_words]

        # lemmatizer = WordNetLemmatizer()
        # lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]

        # return ' '.join(tokens)
