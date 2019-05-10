import os

from .pdf import PDF


def get_file_type_class(path):
    filename, file_extension = os.path.splitext(path)

    if file_extension in ['.pdf']:
        return PDF
    
    
