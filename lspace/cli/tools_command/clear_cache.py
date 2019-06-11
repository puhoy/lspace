import logging

import click

from lspace import db
from lspace.cli.tools_command import tools
from lspace.models.meta_cache import MetaCache

logger = logging.getLogger(__name__)

@tools.command(help='clear metadata cache')
def _clear_cache():
    num = MetaCache.query.delete()
    db.session.commit()
    click.echo('deleted %s rows' % num)
