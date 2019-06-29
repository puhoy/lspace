import logging

import click
import yaml

from lspace.cli.import_command.add_to_shelf_options._options import choose_shelf_other_choices
from lspace.models import Shelf

logger = logging.getLogger(__name__)


def _choose_shelf():
    shelves = Shelf.query.all()
    shelf_names = [shelf.name for shelf in shelves]

    formatted_choices = {}
    for idx, shelf_name in enumerate(shelf_names):
        formatted_choices[str(idx + 1)] = click.style(
            '{index}: {shelf_name}\n'.format(index=idx + 1, shelf_name=shelf_name),
            bold=True)

    for key, val in choose_shelf_other_choices.items():
        formatted_choices[key] = \
            click.style(yaml.dump({
                key: val['explanation']},
                allow_unicode=True), bold=True)

    click.echo(click.style('choose a shelf for this book!', bold=True))
    click.echo(''.join(formatted_choices.values()))
    choices = formatted_choices.keys()

    ret = click.prompt('', type=click.Choice(choices), default='d')

    if ret in list(choose_shelf_other_choices.keys()):
        choice = ret
    else:
        try:
            idx = int(ret) - 1
            choice = shelf_names[idx]
        except Exception as e:
            logger.exception('cant convert %s to int!' % ret, exc_info=True)
            return False

    return choice


def add_to_shelf(book):
    shelf_or_other = _choose_shelf()
    if shelf_or_other in choose_shelf_other_choices.keys():
        f = choose_shelf_other_choices.get(shelf_or_other)['function']
        f(book=book)
    else:
        shelf = Shelf.query.filter_by(name=shelf_or_other).first()
        book.shelf = shelf
