

class BookChoice:
    def __init__(self, d):
        self.d = d

    @property
    def authors(self):
        return self.d['Authors']

    @property
    def title(self):
        return self.d['Title']

    @property
    def isbn13(self):
        return self.d['ISBN-13']

    @property
    def publisher(self):
        return self.d['Publisher']

    @property
    def year(self):
        return self.d['Year']

    @property
    def language(self):
        return self.d['Language']

