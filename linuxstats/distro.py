class Distro:
    """ describes a linux distribution """
    def __init__(self, name, main_page_soup = None, review_page_soup = None,
                 popularity=None, reviews=None):
        self.name = name
        self.main_page_soup = main_page_soup
        self.review_page_soup = review_page_soup
        self.popularity = popularity
        self.reviews = reviews
