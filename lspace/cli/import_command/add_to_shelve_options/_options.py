from lspace.cli.import_command.add_to_shelve_options.put_in_default_shelve import PutInDefaultShelve
from lspace.cli.import_command.add_to_shelve_options.put_in_new_shelve import PutInNewShelve

choose_shelve_other_choices = {
    'n': PutInNewShelve.get_dict(),
    'd': PutInDefaultShelve.get_dict()
}
