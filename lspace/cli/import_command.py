import logging
import os

import click
import isbnlib
from slugify import slugify
from shutil import move, copyfile
import yaml

from ..file_types import get_file_type_class
from ..helpers import query_isbn_data, query_google_books
from ..models.author import Author
from ..models.book import Book
from ..config import library_path, user_config
from . import cli

from ..app import db

run_search = 'run another query'
isbn_lookup = 'lookup by isbn'
specify_manually = 'specify manually'
skip = 'skip'
other_choices = [run_search, isbn_lookup, specify_manually, skip]



@cli.command(name='import', help='import ebooks into your database')
@click.argument('document_path', type=click.Path(exists=True), nargs=-1)
@click.option('--reimport', help='dont check if this file is in the library', default=False, is_flag=True)
@click.option('--move', help='move imported files instead copying', default=False, is_flag=True)
def import_command(document_path, reimport, move):

    for path in document_path:

        file_class = get_file_type_class(path)
        if file_class:
            f = file_class(path)
            
            if not reimport and Book.query.filter_by(md5sum=f.get_md5()).first():
                click.echo('%s already imported, skipping...' % path)
                continue

            click.echo('getting metadata for %s' % path)

            isbns_with_metadata = f.find_in_db()

            if len(isbns_with_metadata) == 0:
                click.echo('could not find any isbn or metadata for %s' % f.filename)
                choice = choose_result(f, [])
                
            elif len(isbns_with_metadata) == 1:
                click.echo('got one result: %s - importing!' % isbns_with_metadata[0])
                choice = isbns_with_metadata[0]

            else:
                choice = choose_result(f, isbns_with_metadata)

            while choice in other_choices:

                if choice == run_search:
                    search_string = click.prompt('search string')
                    results = query_google_books(search_string)

                elif choice == isbn_lookup:
                    results = lookup_isbn()

                if choice != skip:
                    choice = choose_result(f, results)
                else:
                    choice = False

            if choice:
                _import(f, choice, move)
            else:
                click.echo('could not import %s' % path, color='yellow')

        else:
            click.echo('skipping %s' % path)


def lookup_isbn():
    isbn_str = click.prompt(
        'specify isbn (without whitespaces, only the number)')
    result = query_isbn_data(isbn_str)
    if result:
        return [result]
    return []

def choose_result(file_type_object, isbns_with_metadata):
    if not isbns_with_metadata:
        click.echo('no results found :(')
    isbns_with_metadata += other_choices
    formatted_choices = format_metadata_choices(
        isbns_with_metadata)

    click.echo(''.join(formatted_choices))

    ret = click.prompt('choose result for %s' % file_type_object.filename, type=click.IntRange(
        min=1,
        max=len(formatted_choices)))

    idx = ret - 1
    choice = isbns_with_metadata[idx]
    return choice



def _copy_to_library(file_type_object, choice, move_file):
    # prepare the fields for path building
    author_slugs = [slugify(author_name) for author_name in choice['Authors']]
    if not author_slugs:
        author_slugs = ['UNKNOWN AUTHOR']

    AUTHORS = '_'.join(author_slugs)
    TITLE = slugify(choice['Title'])

    logging.debug('author slug: %s' % AUTHORS)
    logging.debug('title slug: %s' % TITLE)

    # create the path for the book
    path_found = False
    count = 0
    path_in_library = False
    while not path_found and count < 100:
        path_in_library = user_config['file_format'].format(
            AUTHORS=AUTHORS, TITLE=TITLE)
        # if, for some reason, the path starts with /, we need to make it relative
        while path_in_library.startswith(os.sep):
            logging.debug('trimming path to %s' % path_in_library[1:])
            path_in_library = path_in_library[1:]

        if count == 0:
            path_in_library += file_type_object.extenstion
        else:
            path_in_library = f'{path_in_library}_{count}{file_type_object.extenstion}'

        target_path = os.path.join(library_path, path_in_library)

        if not os.path.exists(target_path):
            path_found = True

        count += 1
    if not path_in_library:
        logging.error('could not find a path in the library for %s' %
                      file_type_object.path)

    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    logging.debug('importing to %s' % target_path)
    if not move_file:
        copyfile(file_type_object.path, target_path)
    else:
        move(file_type_object.path, target_path)
    
    return path_in_library


def _import(file_type_object, choice, move_file):
    path_in_library = _copy_to_library(file_type_object, choice, move_file)

    authors = []
    for author_name in choice['Authors']:
        author = Author.query.filter_by(name=author_name).first()
        if not author:
            logging.info('creating %s' % author_name)
            author = Author(name=author_name)
            db.session.add(author)
        authors.append(author)
        db.session.commit()

    title = choice['Title']
    isbn13 = choice['ISBN-13']
    publisher = choice['Publisher']
    year = choice['Year']
    language = choice['Language']

    book = db.session.query(Book).filter_by(isbn13=isbn13).first()
    if not book:
        book = Book(
            title=title,
            authors=authors,
            publisher=publisher,
            year=year,
            language=language,
            md5sum=file_type_object.get_md5(),
            path=path_in_library
        )
        logging.info('adding book %s' % book)
        db.session.add(book)
        db.session.commit()
import copy


def format_metadata_choices(isbns_with_metadata):
    isbns_with_metadata = copy.deepcopy(isbns_with_metadata)

    formatted_metadata = []
    for idx, meta in enumerate(isbns_with_metadata):
        logging.info('adding %s' % meta)

        if type(meta) == dict:
            authors = ', '.join([author for author in meta.pop('Authors', [])])
            title = meta.pop('Title')
            formatted_metadata.append(f'\n{idx+1}: {authors} - {title}\n' + yaml.dump(meta, allow_unicode=True))

        else:
            formatted_metadata.append(yaml.dump({idx+1: meta}, allow_unicode=True))
    logging.debug('formatted data is %s' % formatted_metadata)
    return formatted_metadata
