import logging

from lspace import whooshee
from lspace.cli.tools_command import tools

logger = logging.getLogger(__name__)


@tools.command(help='rebuild the search index for your library')
def _rebuild_search_index():
    whooshee.reindex()
