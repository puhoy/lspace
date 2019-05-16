# L-space

a cli ebook manager built around [isbnlib](https://github.com/xlcnd/isbnlib)

currently supports epub and pdf


the whole thing is pretty much just a weekend project, so i would be happy about reported issues or pull requests!


## requirements

just python3 and pip should be fine


## installation

`pip install lspace`


## setup 

after installation, you should run

`lspace init`

this will setup a new configuration file, which you can edit to specify the structure of your library, for example.


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

## why "L-space"?

its named after discworlds [library-space](https://en.wikipedia.org/wiki/List_of_dimensions_of_the_Discworld#L-space) dimension :)