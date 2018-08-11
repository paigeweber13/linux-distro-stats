# third party imports
import urllib.request
from bs4 import BeautifulSoup

# from this package
from .distro import Distro

### CONSTANTS ###
REVIEW_PAGE_BASE_URL = "https://distrowatch.com/dwres.php?resource=ratings&distro="
# temp, will be replaced by titles sourced from a file
linux_distros = [Distro('slackware')]

# functions
def is_review_cell(tag):
    """ checks if a tag is a review cell with certain attributes that are
    unique to review cells on distrowatch.com

    Args:
        tag (BeautifulSoup.tag)
    Returns:
        bool:
    """
    return tag.name == 'td' and tag.has_attr('width') and tag['width'] == '70%'

def get_reviews_page_html(distro_name):
    """ gets html for distrowatch.com review pages for a list of linux distros

    Args:
        distro_name (str): a list distribution name, with the spelling and
                           capitalization used in distrowatch.com links

    Returns:
        str: the html of the page in plaintext
    """
    review_page_html = urllib.request.urlopen(REVIEW_PAGE_BASE_URL + distro_name)
    return review_page_html

def extract_review_text(review_page_html):
    """ gets review text cells from plaintext html and combines all the review
    text into one string """
    soup = BeautifulSoup(review_page_html, "html.parser")
    review_cells = soup.find_all(is_review_cell)
    reviews_text = ''
    for cell in review_cells:
        cell.form.decompose()
        reviews_text += cell.text
        reviews_text += ' '
    # get rid of punctuation
    reviews_text = reviews_text.replace('.', ' ')
    reviews_text = reviews_text.replace('(', ' ')
    reviews_text = reviews_text.replace(')', ' ')
    reviews_text = reviews_text.replace(',', ' ')
    reviews_text = reviews_text.replace('!', ' ')
    reviews_text = reviews_text.replace('?', ' ')
    #get rid of extra whitespace
    reviews_text = ' '.join(reviews_text.split())
    return reviews_text
