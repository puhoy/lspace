from lspace.cli.import_command.import_options.isbn_lookup import ISBNLookup
from lspace.cli.import_command.import_options.manual_import import ManualImport
from lspace.cli.import_command.import_options.manual_search import ManualSearch
from lspace.cli.import_command.import_options.peek import Peek
from lspace.cli.import_command.import_options.skip_book import SkipBook

other_choices = {
    'q': ManualSearch.get_dict(),
    'i': ISBNLookup.get_dict(),
    'p': Peek.get_dict(),
    'm': ManualImport.get_dict(),
    's': SkipBook.get_dict(),
}
