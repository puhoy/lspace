import click
import isbnlib
import yaml

from lspace import db
from lspace import whooshee
from lspace.cli import cli
from lspace.models.meta_cache import MetaCache


@cli.group(help='tools you probably never need... :P')
def tools():
    pass


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


@tools.command(help='rebuild the search index for your library')
def rebuild_search_index():
    whooshee.reindex()


@tools.command(help='clear metadata cache')
def clear_cache():
    num = MetaCache.query.delete()
    db.session.commit()
    click.echo('deleted %s rows' % num)
