import logging

import click
import yaml

from lspace.cli.import_command.add_to_shelve_options._options import choose_shelve_other_choices
from lspace.models import Shelve

logger = logging.getLogger(__name__)


def _choose_shelve():
    shelves = Shelve.query.all()
    shelve_names = [shelve.name for shelve in shelves]

    formatted_choices = {}
    for idx, shelve_name in enumerate(shelve_names):
        formatted_choices[str(idx + 1)] = click.style(
            '{index}: {shelve_name}\n'.format(index=idx + 1, shelve_name=shelve_name),
            bold=True)

    for key, val in choose_shelve_other_choices.items():
        formatted_choices[key] = \
            click.style(yaml.dump({
                key: val['explanation']},
                allow_unicode=True), bold=True)

    click.echo(click.style('choose a shelve for this book!', bold=True))
    click.echo(''.join(formatted_choices.values()))
    choices = formatted_choices.keys()

    ret = click.prompt('', type=click.Choice(choices), default='d')

    if ret in list(choose_shelve_other_choices.keys()):
        choice = ret
    else:
        try:
            idx = int(ret) - 1
            choice = shelve_names[idx]
        except Exception as e:
            logger.exception('cant convert %s to int!' % ret, exc_info=True)
            return False

    return choice


def add_to_shelve(book):
    shelve_or_other = _choose_shelve()
    if shelve_or_other in choose_shelve_other_choices.keys():
        f = choose_shelve_other_choices.get(shelve_or_other)['function']
        f(book=book)
    else:
        shelve = Shelve.query.filter_by(name=shelve_or_other).first()
        book.shelve = shelve
