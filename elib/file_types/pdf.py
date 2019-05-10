import re
import string
from typing import List

import isbnlib
import PyPDF2 as pypdf
import requests

# pdf = PDF('/home/meatpuppet/ebooks/books/computerei/Beautiful Code.pdf')
# print(pdf.find_isbn())
# print(pdf.get_metadata())
from elib.file_types._base import FileTypeBase


class PDF(FileTypeBase):
    extenstion = '.pdf'
    
    def __init__(self, path):
        super().__init__(path)

        self.pdf_reader = pypdf.PdfFileReader(self.path)
        self.metadata = self.pdf_reader.getDocumentInfo()

    def get_text(self) -> List[str]:
        pages = []

        # printing number of pages in pdf file
        for page_idx in range(self.pdf_reader.numPages):

            page = self.pdf_reader.getPage(page_idx)

            extracted_text = page.extractText()
            pages.append(extracted_text)

        # if true, there was at least one page with text
        if True in [True if page else False for page in pages]:
            return pages
        return []

    def get_author(self):
        self.metadata.author

    def get_title(self):
        self.metadata.title
