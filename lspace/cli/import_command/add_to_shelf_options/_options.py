from lspace.cli.import_command.add_to_shelf_options.put_in_default_shelf import PutInDefaultShelf
from lspace.cli.import_command.add_to_shelf_options.put_in_new_shelf import PutInNewShelf

choose_shelf_other_choices = {
    'n': PutInNewShelf.get_dict(),
    'd': PutInDefaultShelf.get_dict()
}
