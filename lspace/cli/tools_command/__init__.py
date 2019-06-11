import logging

import click
import isbnlib
import yaml

from lspace.cli import cli

logger = logging.getLogger(__name__)


@cli.group(help='tools you probably never need... :P')
def tools():
    pass


from lspace.cli.tools_command.clear_cache import _clear_cache
from lspace.cli.tools_command.rebuild_search_index import _rebuild_search_index
from lspace.cli.tools_command.update_paths import _update_paths


@tools.command(help='convert isbn-10 to isbn-13')
@click.argument('dirtyisbn')
def convert_to_isbn13(dirtyisbn):
    click.echo(isbnlib.to_isbn13(dirtyisbn))


@tools.command(help='find metadata for books by words')
@click.argument('words')
def find_meta_by_text(words):
    if isbnlib.is_isbn13:
        click.echo('%s looks like isbn!' % words)
        results = isbnlib.meta(words, service='openl')
    else:
        results = isbnlib.goom(words)
    click.echo(yaml.dump(results))


@tools.command(help='start ipython')
def shell():
    import pdb
    import rlcompleter, readline
    readline.parse_and_bind('tab: complete')

    pdb.Pdb.complete = rlcompleter.Completer(locals()).complete

    breakpoint()
