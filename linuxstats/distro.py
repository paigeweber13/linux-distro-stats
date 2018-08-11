class Distro:
    """ describes a linux distribution """
    def __init__(self, name=None,
                 popularity=None,
                 reviews=None):
        self.name = name
        self.popularity = popularity
        self.reviews = reviews
