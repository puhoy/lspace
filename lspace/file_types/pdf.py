from typing import List

import PyPDF2 as pypdf

from ._base import FileTypeBase


class PDF(FileTypeBase):
    extension = '.pdf'

    def __init__(self, path):
        super().__init__(path)

        self.pdf_reader = pypdf.PdfFileReader(self.path)
        self.metadata = self.pdf_reader.getDocumentInfo()
        self.xmp_metadata = self.pdf_reader.getXmpMetadata()

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
        # meta = self.pdf_reader.xmpMetadata

        # never found a pdf with xmp metadata - not sure what the results would look like
        # if meta:
        #    if meta.dc_description:
        #        print(meta.dc_description)
        return None

    def get_author(self):
        if self.metadata:
            return self.metadata.author
        return None

    def get_title(self):
        if (self.xmp_metadata and
                self.xmp_metadata.dc_title and
                self.xmp_metadata.dc_title.get('x-default', False)):
            return self.xmp_metadata.dc_title.get('x-default', False)

        if self.metadata:
            return self.metadata.title
        return None
