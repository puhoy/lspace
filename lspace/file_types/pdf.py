
from typing import List

import PyPDF2 as pypdf

from ._base import FileTypeBase


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
        if True in [bool(page) for page in pages]:
            return pages
        return []

    def get_isbn(self):
        meta = self.pdf_reader.getXmpMetadata()
        # never found a pdf with xmp metadata - not sure what the results would look like
        #if meta:
        #    if meta.dc_description:
        #        print(meta.dc_description)
        return None

    def get_author(self):
        return self.metadata.author

    def get_title(self):
        return self.metadata.title
