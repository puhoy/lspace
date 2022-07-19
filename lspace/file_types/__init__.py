import os
from pathlib import Path

from ._base import FileTypeBase
from .pdf import PDF
from .epub import Epub

mapping = {
    '.pdf': PDF,
    '.epub': Epub
}


def get_file_type_object(path):
    # type: (Path) -> FileTypeBase
    file_extension = path.suffix

    file_class = mapping.get(file_extension, None)
    if file_class:
        return file_class(str(path))
    else:
        return None
