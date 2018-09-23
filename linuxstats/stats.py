# python imports
from datetime import date
import re
import urllib.request

# third party imports
from bs4 import BeautifulSoup

# from this package
from .distro import Distro

### CONSTANTS ###
REVIEW_PAGE_BASE_URL = "https://distrowatch.com/dwres.php?resource=ratings&distro="
MAIN_PAGE_BASE_URL = "https://distrowatch.com/table.php?distribution="
# temp, will be replaced by titles sourced from a file
LINUX_DISTROS = [Distro('slackware')]

### functions ###
# get soups
def get_reviews_page_html_soup(distro_name):
    """ gets html for distrowatch.com review pages for a list of linux distros

    Args:
        distro_name (str): a list distribution name, with the spelling and
                           capitalization used in distrowatch.com links

    Returns:
        soup: a 'soup' of the html from the reviews page that is parseable by
              BeautifulSoup4
    """
    review_page_html = urllib.request.urlopen(REVIEW_PAGE_BASE_URL + distro_name)
    soup = BeautifulSoup(review_page_html, 'html.parser')
    return soup

def get_main_page_html_soup(distro_name):
    """ gets html of main distrowatch page """
    main_page_html = urllib.request.urlopen(MAIN_PAGE_BASE_URL + distro_name)
    soup = BeautifulSoup(main_page_html, 'html.parser')
    return soup

# Reviews
def is_review_cell(tag):
    """ checks if a tag is a review cell with certain attributes that are
    unique to review cells on distrowatch.com

    Args:
        tag (BeautifulSoup.tag)
    Returns:
        bool:
    """
    return tag.name == 'td' and tag.has_attr('width') and tag['width'] == '70%'

def extract_review_text(review_page_soup):
    """ gets review text cells from plaintext html and combines all the review
    text into one string """
    review_cells = review_page_soup.find_all(is_review_cell)
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

# ratings
def is_rating_cell(tag):
    """ checks if tag holds a rating """
    return tag.name == 'td' and tag.has_attr('width') and tag['width'] == '30%'

def extract_ratings(review_page_soup):
    rating_cells = review_page_soup.find_all(is_rating_cell)
    ratings = {}
    rating_regex = re.compile(r"""
            Rating:(?P<rating>\d+)
            Date:(?P<year>\d+)-(?P<month>\d+)-(?P<day>\d+)
            Votes""", re.VERBOSE)
    for cell in rating_cells:
        text = ''.join(cell.text.split())
        result = rating_regex.search(text)
        rating_date = date(int(result.group('year')),
                           int(result.group('month')),
                           int(result.group('day')))
        print(rating_date)
        ratings[rating_date] = int(result.group('rating'))
    return ratings

# popularity metric
def extract_popularity(main_page_soup):
    info_cell = main_page_soup.find("td", class_="TablesTitle")
    text = ''.join(info_cell.text.split())
    popularity_regex = re.compile(r"""
        Popularity\(hitsperday\).*
        12months:(?P<twelve_month_score>\d+).*
        6months:(?P<six_month_score>\d+).*
        3months:(?P<three_month_score>\d+).*
        4weeks:(?P<four_week_score>\d+).*
        1week:(?P<one_week_score>\d+)
        """, re.VERBOSE)
    print('text:')
    print(text)
    print('regex:')
    print(popularity_regex)
    result = popularity_regex.search(text)
    print('result')
    print(result)
    popularity = {'1w':int(result.group('one_week_score')),
                  '4w':int(result.group('four_week_score')),
                  '3m':int(result.group('three_month_score')),
                  '6m':int(result.group('six_month_score')),
                  '12m':int(result.group('twelve_month_score')), }
    return popularity
