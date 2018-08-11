# third party imports
import urllib.request
from bs4 import BeautifulSoup

# from this package
from .distro import Distro

### CONSTANTS ###
REVIEW_PAGE_BASE_URL = "https://distrowatch.com/dwres.php?resource=ratings&distro="
# temp, will be replaced by text from a file
#distrosToCheck = ["slackware"]
linux_distros = [Distro('slackware')]

# functions
def is_review_cell(tag):
    return tag.name == 'td' and tag.has_attr('width') and tag['width'] == '70%'

# def getReviewsPagesHtml(distroNames):
    """ gets html for distrowatch.com review pages for a list of linux distros

    arguments:
    distroNames -- a list of distribution names, with the spelling and
                   capitalization used in distrowatch.com links

    return value: a dictionary where keys are distro names and values are
                  httpResponse objects
    """

    # reviewPageHtml = {}
    # for distro in distroNames:
    #     reviewPageHtml[distro] = urllib.request.urlopen(
    #         REVIEW_PAGE_BASE_URL + distro)
    # print(reviewPageHtml)
    # print(reviewPageHtml["slackware"].read())
    # return reviewPageHtml

def get_reviews_page_html(distro_name):
    review_page_html = urllib.request.urlopen(REVIEW_PAGE_BASE_URL + distro_name)
    return review_page_html

def extractReviewText(review_page_html):
    soup = BeautifulSoup(review_page_html, "html.parser")
    review_cells = soup.find_all(is_review_cell)
    reviews_text = ''
    for cell in review_cells:
        cell.form.decompose()
        reviews_text += cell.text
        reviews_text += ' '
    reviews_text = reviews_text.replace('\n', ' ')
    reviews_text = reviews_text.replace('\r', ' ')
    reviews_text = reviews_text.replace('.', ' ')
    reviews_text = reviews_text.replace('(', ' ')
    reviews_text = reviews_text.replace(')', ' ')
    reviews_text = reviews_text.replace(',', ' ')
    reviews_text = reviews_text.replace('!', ' ')
    reviews_text = reviews_text.replace(',', ' ')

    # html = htmlDictionary['slackware'].read()
    # html = htmlDictionary['slackware']
    # soup = BeautifulSoup(html, "html.parser")
    # reviewText = soup.select('td[width="70%"]')

    return reviews_text

# main
#import os
def main():
    #print(os.environ['PYTHONPATH'].split(os.pathsep))
    return "<body>hello from python</body>"
    #return extractReviewText(get_reviews_page_html(distros_to_check[0]))

if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
