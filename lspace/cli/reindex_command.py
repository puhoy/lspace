
from . import cli
from ..app import whooshee

@cli.command()
def reindex():
    whooshee.reindex()
