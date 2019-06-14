from lspace.cli.import_command.add_to_shelve_helpers.put_in_default_shelve import PutInDefaultShelve
from lspace.cli.import_command.add_to_shelve_helpers.put_in_new_shelve import PutInNewShelve
from lspace.cli.import_command.import_helpers.isbn_lookup import ISBNLookup
from lspace.cli.import_command.import_helpers.manual_import import ManualImport
from lspace.cli.import_command.import_helpers.manual_search import ManualSearch
from lspace.cli.import_command.import_helpers.peek import Peek
from lspace.cli.import_command.import_helpers.skip_book import SkipBook

other_choices = {
    'q': ManualSearch.get_dict(),
    'i': ISBNLookup.get_dict(),
    'p': Peek.get_dict(),
    'm': ManualImport.get_dict(),
    's': SkipBook.get_dict(),
}

choose_shelve_other_choices = {
    'n': PutInNewShelve.get_dict(),
    'd': PutInDefaultShelve.get_dict()
}
