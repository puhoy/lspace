class SearchResult:
    """
    wraps isbnlib search results

    {'ISBN-13': '9781593276409',
    'Title': 'Doing Math With Python',
    'Authors': ['Amit Saha'],
    'Publisher': 'No Starch Press',
    'Year': '2015',
    'Language': 'en'}
    """

    def __init__(self, d=None, isbn_source='', metadata_source=''):
        if d is None:
            d = {}
        self.from_dict(d)
        self.isbn_source = isbn_source
        self.metadata_source = metadata_source

    def from_dict(self, d):
        self.isbn = d.get('ISBN-13', None)
        self.title = d.get('Title', 'no title')
        self.publisher = d.get('Publisher', None)
        self.year = d.get('Year', 'no year')
        self.language = d.get('Language', None)
        if not d.get('Authors', None):
            self.authors = ['no author']
        else:
            self.authors = d.get('Authors')
    def __repr__(self):
        return '<isbn={isbn} authors={authors} title={title}>'.format(isbn=self.isbn, authors=self.authors,
                                                                      title=self.title)

    def formatted_output_head(self):
        authors = ', '.join([author for author in self.authors])
        title = self.title
        return '{authors} - {title} ({year})'.format(
            authors=authors, title=title, year=self.year)

    def formatted_output_details(self):
        return 'isbn: {isbn}\npublisher: {publisher}\nlanguage: {language}\nmetadata source: {source}\n'.format(isbn=self.isbn,
                                                                                     language=self.language,
                                                                                     publisher=self.publisher,
                                                                                     source=self.metadata_source)