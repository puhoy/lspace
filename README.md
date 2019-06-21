# L-space

a cli ebook manager built around [isbnlib](https://github.com/xlcnd/isbnlib)

currently supports epub and pdf


[![Build Status](https://travis-ci.org/puhoy/lspace.svg?branch=master)](https://travis-ci.org/puhoy/lspace)

[![codecov](https://codecov.io/gh/puhoy/lspace/branch/master/graph/badge.svg)](https://codecov.io/gh/puhoy/lspace)

## requirements

python >=3.4 and pip should be fine


## installation

`pip install lspace`


## setup 

after installation, you should run

`lspace init`

this will setup a new configuration file, which you can edit to specify the structure of your library, for example.

a default config file would look like this:
```
database_path: sqlite:////home/USER/.config/lspace/lspace.db
file_format: '{SHELVE}/{AUTHORS}_{TITLE}'
library_path: ~/library
loglevel: error
default_shelve: misc
default_author: no author
default_language: no language
default_publisher: no publisher
```

#### database path

path to your database. 
the project uses sqlalchemy, so all databases supported by sqlalchemy should be fine.

#### file_format

template string for storing the plain files in the library.

`{SHELVE}/{AUTHORS}_{TITLE}` would produce files like `scifi/cixin-liu_three-body-problem.epub`

author and title will be automatically slugified for this.

possible variables to use are: AUTHORS, TITLE, SHELVE, YEAR, LANGUAGE, PUBLISHER

#### library path

where the imported files are stored

#### loglevel

the default python loglevels (debug, info, error, exception)

#### default_{shelve, author, language, publisher}

the default field names, in case nothing is specified in import


## usage

### importing

`lspace import path/to/ebook.epub`

`lspace import path/to/folder/*`

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

# change the database path! (otherwise it would still use the regular db)
sed -i 's/lspace\/lspace.db/lspace_dev\/lspace.db/g' ~/.config/lspace_dev/config.yml

# also, if you want, set the loglevel to something else
``` 
    
after this, just set LSPACE_CONFIG to your new config file before you start to try new stuff

```
export LSPACE_CONFIG=~/.config/lspace_dev/config.yml  # bash
set -gx LSPACE_CONFIG ~/.config/lspace_dev/config.yml  # fish 
```

## why "L-space"?

its named after discworlds [library-space](https://en.wikipedia.org/wiki/List_of_dimensions_of_the_Discworld#L-space) dimension :)