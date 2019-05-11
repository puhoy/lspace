import logging

import click
import isbnlib
import yaml

from . import cli


@cli.command()
@click.argument('dirtyisbn')
def convert_to_isbn13(dirtyisbn):
    click.echo(isbnlib.to_isbn13(dirtyisbn))


@cli.command()
@click.argument('words')
def find_meta_by_text(words):
    if isbnlib.is_isbn13:
        click.echo('%s looks like isbn!' % words)
        results = isbnlib.meta(words, service='openl')
    else:
        results = isbnlib.goom(words)
    click.echo(yaml.dump(results))

