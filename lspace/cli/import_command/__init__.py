import click

from lspace.cli import cli
from lspace.cli.import_command._import import import_wizard


@cli.command(name='import', help='import ebooks into your database')
@click.argument('document_path', type=click.Path(), nargs=-1)
@click.option('--skip-library-check', help='dont check if this file is in the library already', default=False,
              is_flag=True)
@click.option('--move', help='move imported files instead copying', default=False, is_flag=True)
@click.option('--inplace', help='add this file to the library, but keep it where it is', default=False, is_flag=True)
def import_command(document_path, skip_library_check, move, inplace):
    for path in document_path:
        import_wizard(path, skip_library_check, move, inplace)
