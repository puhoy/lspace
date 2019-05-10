
import logging
import os

import click
import yaml
from pick import pick

from .file_types import get_file_type_class

import logging

logging.basicConfig(format='%(asctime)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S', level=logging.DEBUG)


@click.group()
def cli():
    pass


@cli.command()
@click.argument('document_path', type=click.Path(exists=True), nargs=-1)
def get_isbn(document_path):

    for path in document_path:
        click.prompt

        file_class = get_file_type_class(path)
        if file_class:
            click.echo('getting metadata for %s' % path)
            f = file_class(path)

            isbns_with_metadata = f.find_in_db()
            formatted_choices = format_metadata_choices(isbns_with_metadata)

            click.echo('found metadata for %s\n' % path)
            click.echo('\n'.join(formatted_choices))

            ret = click.prompt('', type=click.IntRange(
                min=1,
                max=len(formatted_choices)))
            
            idx = ret - 1
            choice = isbns_with_metadata[idx]
            print(choice)

        else:
            click.echo('skipping %s' % path)


def format_metadata_choices(isbns_with_metadata):
    formatted_metadata = []
    for idx, meta in enumerate(isbns_with_metadata):
        logging.debug('adding %s' % meta)
        formatted_metadata.append(yaml.dump({idx+1: meta}))
    logging.debug('formatted data is %s' % formatted_metadata)
    return formatted_metadata
