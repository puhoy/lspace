import logging
import os
import shutil
import subprocess

import click
from slugify import slugify

from flask import current_app
from lspace.cli import cli
from lspace.helpers import find_unused_path
from lspace.helpers.query import query_db

logger = logging.getLogger(__name__)


@cli.command(help='export books to a folder - this uses ebook-convert, which is part of calibre')
@click.argument('query', nargs=-1)
@click.argument('export_path')
@click.option('--format')
def export(query, export_path, format):
    if not shutil.which('ebook-convert'):
        click.echo('could not find ebook-convert executable! is calibre installed?')
        return
    export_path = os.path.abspath(os.path.expanduser(export_path))
    click.echo('exporting to %s' % export_path)

    if not os.path.isdir(export_path):
        click.echo('path has to be a folder!')
        return

    if not format.startswith('.'):
        # format and extension should both start with '.'
        format = '.' + format

    results = query_db(query)
    for result in results:
        author_slugs = [slugify(author.name) for author in result.authors]
        if not author_slugs:
            author_slugs = ['UNKNOWN AUTHOR']
        authors_slug = '_'.join(author_slugs)

        authors_str = '_'.join([author.name for author in result.authors])
        title_slug = slugify(result.title)

        if format and format != result.extension:
            target_extension = format
        else:
            target_extension = result.extension

        target_in_export_path = find_unused_path(export_path,
                                                 current_app.config['USER_CONFIG']['file_format'],
                                                 authors_slug,
                                                 title_slug,
                                                 target_extension)
        target_path = os.path.join(export_path, target_in_export_path)
        if not os.path.isdir(os.path.dirname(target_path)):
            os.makedirs(os.path.dirname(target_path))

        if target_extension != result.extension:
            click.echo('converting %s to %s' % (result.extension, format))
            try:
                subprocess.call(
                    ["ebook-convert",
                     result.full_path,
                     target_path
                     ])
            except Exception as e:
                logger.exception('error converting %s' % result.full_path, exc_info=True)
        else:
            click.echo('exporting {authors_str} - {result.title} to {target_path}'.format(authors_str=authors_str,
                                                                                          result=result,
                                                                                          target_path=target_path))
            shutil.copyfile(result.full_path, target_path)
    return
