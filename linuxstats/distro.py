class Distro:
    """ describes a linux distribution """
    """
    metrics (dict) contains:
            popularity (dict): popularity metric. Eventually I will fetch the
                               one week popularity once a week and store it so
                               I can create my own popularity metrics over any
                               length of time. Currently maps 12m, 6m, 3m, 4w,
                               and 1w to a popularity score
            ratings (dict): maps date to rating
            easy (dict): maps date of review to how much that review added to
                         this score
            reliable (dict): maps date to metric contribution
            fast (dict): maps date to contribution
            customizable (dict): maps date to contribution
    """

    def __init__(self, name,
                 main_page_soup=None, review_page_soup=None,
                 popularity=None, ratings=None, reviews=None, metrics=None):
        self.name = name
        self.metrics = metrics
