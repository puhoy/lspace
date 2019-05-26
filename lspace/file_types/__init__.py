import os

from ._base import FileTypeBase
from .pdf import PDF
from .epub import Epub

mapping = {
    '.pdf': PDF,
    '.epub': Epub
}


def get_file_type_class(path):
    filename, file_extension = os.path.splitext(path)

    file_class = mapping.get(file_extension, None)
    return file_class
