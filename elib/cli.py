
import logging
import os
from shutil import copyfile, move

import click
import isbnlib
import yaml
from pick import pick
from slugify import slugify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .file_types import get_file_type_class
from .models import Base
from .models.author import Author
from .models.book import Book
from .models.book_author_association import book_author_association_table

APP_NAME = 'elib'
CONFIG_FILE = 'config.yaml'

app_dir = click.get_app_dir(APP_NAME)


run_search = 'run another query'
isbn_lookup = 'lookup by isbn'
specify_manually = 'specify manually'
skip = 'skip'
other_choices = [run_search, isbn_lookup, specify_manually, skip]


def get_default_config():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(this_dir, 'default_conf.yaml'), 'r') as default_config_file:
        default_config = yaml.load(default_config_file)
        default_config['database'] = default_config['database'].format(APP_DIR=app_dir)
    return default_config


def make_db_session(db_path):
    engine = create_engine(db_path, echo=True)
    Session = sessionmaker(bind=engine)

    logging.info('creating engine...')
    Base.metadata.create_all(engine)

    return Session()


@click.group()
def cli():
    pass


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
    

@cli.command()
def init():
    os.makedirs(app_dir, exist_ok=True)
    config_path = os.path.join(app_dir, CONFIG_FILE)
    if os.path.exists(config_path):
        click.prompt('config exists - override?',
                     default=False, confirmation_prompt=True)

    default_config = get_default_config()
    with open(config_path, 'w') as config:
        yaml.dump(default_config, config)


def read_config():
    config_path = os.path.join(app_dir, CONFIG_FILE)
    with open(config_path, 'r') as config:
        conf = yaml.load(config)

    conf = {**get_default_config(), **conf}

    loglevel = logging._nameToLevel[conf.get('loglevel', 'INFO')]
    logging.basicConfig(format='%(asctime)s - %(message)s',
                        datefmt='%d-%b-%y %H:%M:%S', level=loglevel)

    session = make_db_session(conf['database'])

    return conf, session


@cli.command(name='import')
@click.argument('document_path', type=click.Path(exists=True), nargs=-1)
@click.option('--reimport', help='dont check if this file is in the library', default=False, is_flag=True)
@click.option('--move', help='move imported files instead copying', default=False, is_flag=True)
def _import(document_path, reimport, move):
    config, session = read_config()

    for path in document_path:

        file_class = get_file_type_class(path)
        if file_class:
            f = file_class(path)
            if not reimport and session.query(Book).filter_by(md5sum=f.get_md5()).first():
                logging.info('%s already imported, skipping...' % path)
                continue

            click.echo('getting metadata for %s' % path)

            isbns_with_metadata = f.find_in_db()
            
            
            if len(isbns_with_metadata) == 0:
                choice = False

            elif len(isbns_with_metadata) == 1:
                choice = isbns_with_metadata[0]

            else:
                choice = choose_result(f, isbns_with_metadata)
            
            while choice in other_choices:
                if choice == run_search:
                    search_string = click.prompt('search string')
                    results = query_google_books(search_string)
                    
                elif choice == skip:
                    continue
                elif choice == isbn_lookup:
                    results = lookup_isbn()

                choice = choose_result(f, results)
                
            if choice:
                print(choice)
                _import(f, choice, config, session, move)
        else:
            click.echo('skipping %s' % path)

def lookup_isbn():
    isbn_str = click.prompt('specify isbn (without whitespaces, only the number)')
    if isbnlib.is_isbn10(isbn_str):
        isbn_str = isbnlib.to_isbn13(isbn_str)
    try:
        meta = isbnlib.meta(isbn_str, service='openl', cache='default')
    except isbnlib.dev._exceptions.NoDataForSelectorError:
        meta = {}
    if not meta:
        try:
            meta = isbnlib.meta(isbn_str, service='goob', cache='default')
        except isbnlib.dev._exceptions.NoDataForSelectorError:
            meta = {}
    if meta:
        return [meta]
    else:
        return []

def choose_result(file_type_object, isbns_with_metadata):
    isbns_with_metadata += other_choices
    formatted_choices = format_metadata_choices(
        isbns_with_metadata)

    click.echo('\n'.join(formatted_choices))

    ret = click.prompt('choose result for %s' % file_type_object.filename, type=click.IntRange(
        min=1,
        max=len(formatted_choices)))

    idx = ret - 1
    choice = isbns_with_metadata[idx]
    return choice

def query_google_books(words):
    return isbnlib.goom(words)

def _import(file_type_object, choice, conf, session, move_file):
    library_path = os.path.abspath(os.path.expanduser(conf['library_path']))
    os.makedirs(library_path, exist_ok=True)

    # prepare the fields for path building
    author_slugs = [slugify(author_name) for author_name in choice['Authors']]

    AUTHORS = '_'.join(author_slugs)
    TITLE = choice['Title']

    # create the path for the book
    path_found = False
    count = 0
    path_in_library = False
    while not path_found and count < 100:
        path_in_library = conf['file_format'].format(
            AUTHORS=AUTHORS, TITLE=TITLE)
        if count == 0:
            path_in_library += file_type_object.extenstion
        else:
            path_in_library = f'{path_in_library}_{count}.{file_type_object.extenstion}'

        target_path = os.path.join(library_path, path_in_library)

        if not os.path.exists(target_path):
            path_found = True

        count += 1
    if not path_in_library:
        logging.error('could not find a path in the library for %s' %
                      file_type_object.path)

    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    if not move_file:
        copyfile(file_type_object.path, target_path)
    else:
        move(file_type_object.path, target_path)

    authors = []
    for author_name in choice['Authors']:
        author = session.query(Author).filter_by(name=author_name).first()
        if not author:
            logging.info('creating %s' % author_name)
            author = Author(name=author_name)
            session.add(author)
        authors.append(author)
        session.commit()

    title = choice['Title']
    isbn_13 = choice['ISBN-13']
    publisher = choice['Publisher']
    year = choice['Year']
    language = choice['Language']

    book = session.query(Book).filter_by(isbn_13=isbn_13).first()
    if not book:
        logging.info('adding book %s' % book)
        book = Book(
            title=title,
            authors=authors,
            publisher=publisher,
            year=year,
            language=language,
            md5sum=file_type_object.get_md5(),
            path=path_in_library
        )
        session.add(book)
        session.commit()


def format_metadata_choices(isbns_with_metadata):
    formatted_metadata = []
    for idx, meta in enumerate(isbns_with_metadata):
        logging.debug('adding %s' % meta)
        formatted_metadata.append(yaml.dump({idx+1: meta}, allow_unicode=True))
    logging.debug('formatted data is %s' % formatted_metadata)
    return formatted_metadata
