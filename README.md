# L-Space

a cli ebook manager built around [isbnlib](https://github.com/xlcnd/isbnlib)

when importing it tries to find isbns in the files metadata and in the text 
to fetch correct metadata about the book. 
also, it gets metadata from google books and openlibrary based on the filename.

after this, your properly renamed files will be stored in your library folder.


currently supports epub and pdf.


[![Build Status](https://travis-ci.org/puhoy/lspace.svg?branch=master)](https://travis-ci.org/puhoy/lspace)

[![codecov](https://codecov.io/gh/puhoy/lspace/branch/master/graph/badge.svg)](https://codecov.io/gh/puhoy/lspace)

## requirements

python >=3.5 and pip should be fine


## installation

#### from pypi (latest release)

`pip install lspace`

#### from github (probably-not-so-stable-dev-stuff)

`pip install git+https://github.com/puhoy/lspace.git`


## setup 

after installation, you should run

`lspace init`

this will setup a new configuration file, which you can edit to specify the structure of your library, for example.

a default config file would look like this:
```
database_path: sqlite:////home/USER/.config/lspace/lspace.db
file_format: '{SHELF}/{AUTHORS}_{TITLE}'
library_path: ~/library
loglevel: error
default_shelf: misc
default_author: no author
default_language: no language
default_publisher: no publisher
```

#### database path

path to your database. 
the project uses sqlalchemy, so all databases supported by sqlalchemy should be fine.

#### file_format

template string for storing the plain files in the library.

`{SHELF}/{AUTHORS}_{TITLE}` would produce files like `scifi/cixin-liu_three-body-problem.epub`

author and title will be automatically slugified for this.

possible variables to use are: AUTHORS, TITLE, SHELF, YEAR, LANGUAGE, PUBLISHER

#### library path

where the imported files are stored

#### loglevel

the default python loglevels (debug, info, error, exception)

#### default_{shelf, author, language, publisher}

the default field names, in case nothing is specified in import


## usage

### importing

`lspace import path/to/ebook.epub`

`lspace import path/to/folder/*`

#### import from calibre library

`lspace import path/to/calibre_library/metadata.db`


### searching your library

`lspace list QUERY [--path]`

for example, 

`lspace list programming --path`

would return something like

    /home/USER/library/donald-e-knuth/art-of-computer-programming-volume-2.pdf
    /home/USER/library/donald-e-knuth/the-art-of-computer-programming-volume-1-fascicle-1.pdf

and 

`lspace list dwarf`

would return return

    Peter Tyson - Getting Started With Dwarf Fortress

### removing stuff

`lspace remove QUERY`

this command will ask you before it actually deletes stuff :)

    Peter Tyson - Getting Started With Dwarf Fortress
    /home/USER/library/peter-tyson/getting-started-with-dwarf-fortress.epub
    delete this book from library? [y/N]:

### exporting books


`lspace export QUERY ~/some/folder/ --format mobi`

would convert all books matching on QUERY to 'mobi' and export them to ~/some/folder

to actually export to another format, you need "ebook-convert", which is part of [calibre](https://calibre-ebook.com/)!

## setting up a dev env

#### 1. clone this repo 

#### 2. make a virtualenv and activate it

```
virtualenv  env --python=python

source env/bin/activate  # for bash

# or
#. env/bin/activate.fish  # for fish
```

#### 3. install requirements

```
    pip install  -e .[dev]
```

#### 4. set up a separate config to not mess up your regular installation

```
# initialize a new config file at a separate path
LSPACE_CONFIG=~/.config/lspace_dev/config.yml lspace init

# change the database and library path! (otherwise it would still use the regular db)
sed -i 's/lspace\/lspace.db/lspace_dev\/lspace.db/g' ~/.config/lspace_dev/config.yml
sed -i 's/~\/library/~\/library_dev/g' ~/.config/lspace_dev/config.yml

# also, if you want, set the loglevel to something else
``` 
    
after this, just set LSPACE_CONFIG to your new config file before you start to try new stuff

```
export LSPACE_CONFIG=~/.config/lspace_dev/config.yml  # bash
set -gx LSPACE_CONFIG ~/.config/lspace_dev/config.yml  # fish 
```

## why "L-space"?

its named after discworlds [library-space](https://en.wikipedia.org/wiki/List_of_dimensions_of_the_Discworld#L-space) dimension :)