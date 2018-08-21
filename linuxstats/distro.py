"""
    popularity (dict): 12 month, 6 month, 3 month, 4 week, and 1 week
                       popularity metric. Eventually I will fetch the one week
                       popularity once a week and store it so I can create my
                       own popularity metrics over any length of time
                       maps 12m, 6m, 3m, 4w, and 1w to popularity score
    ratings (dict): maps date to rating
    reviews (str): plaintext content of reviews
"""
class Distro:
    """ describes a linux distribution """
    def __init__(self, name, main_page_soup=None, review_page_soup=None,
                 popularity=None, ratings=None, reviews=None):
        self.name = name
        self.main_page_soup = main_page_soup
        self.review_page_soup = review_page_soup
        self.popularity = popularity
        self.ratings = ratings
        self.reviews = reviews
