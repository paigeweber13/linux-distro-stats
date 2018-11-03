# python imports
from datetime import date
import json
import pdb
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

# Reviews (and the metrics gained from them)
def is_review_row(tag):
    return tag.has_attr('style') and tag['style'] == 'outline: thin solid black'

def extract_reviews(review_page_soup):
    # review_cells = review_page_soup.find_all(is_review_cell)
    review_rows = review_page_soup.find_all(is_review_row)
    # reviews_text = ''
    reviews = {}
    date_regex = re.compile(r"""
            Date:(?P<year>\d+)-(?P<month>\d+)-(?P<day>\d+)""", re.VERBOSE)
    for row in review_rows:
        text = ''.join(row.td.text.split())
        result = date_regex.search(text)
        review_date = date(int(result.group('year')),
                           int(result.group('month')),
                           int(result.group('day')))
        # TODO: find a non-destructive way to do this
        # actually, is this destructive? This looks like it just destroys
        # review_rows, not the original review_page_soup, though review_rows
        # may only be a shallow copy....
        row.td.decompose()
        row.td.form.decompose()
        review_text = row.td.text
        # get rid of punctuation
        review_text = review_text.replace('.', ' ')
        review_text = review_text.replace('(', ' ')
        review_text = review_text.replace(')', ' ')
        review_text = review_text.replace(',', ' ')
        review_text = review_text.replace('!', ' ')
        review_text = review_text.replace('?', ' ')
        #get rid of extra whitespace
        review_text = ' '.join(review_text.split())
        reviews[review_date] = review_text.split()
    return reviews

def build_keyword_metrics(review_page_soup):
    #pdb.set_trace()
    metrics = {}
    reviews = extract_reviews(review_page_soup)
    with open('keywords.json') as keyword_file:
        keyword_dict = json.load(keyword_file)
    # TODO: Complexity is 2n^4. Yikes. Make it better.
    for metric in keyword_dict:
        metrics[metric] = {}
        for review_date, review in reviews.items():
            score = 0
            for word in review:
                for keyword in keyword_dict[metric]['for']:
                    if word == keyword:
                        score += 1
                for keyword in keyword_dict[metric]['against']:
                    if word == keyword:
                        score -= 1
            metrics[metric][review_date] = score
    return metrics

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
        # print(rating_date)
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
    popularity = {'1w': int(result.group('one_week_score')),
                  '4w': int(result.group('four_week_score')),
                  '3m': int(result.group('three_month_score')),
                  '6m': int(result.group('six_month_score')),
                  '12m': int(result.group('twelve_month_score')), }
    return popularity

# builds a distro object with all the key statistics
def build_distro(distro_name):
    review_page_soup = get_reviews_page_html_soup(distro_name)
    main_page_soup = get_main_page_html_soup(distro_name)
    discovered_metrics = {}
    discovered_metrics['popularity'] = extract_popularity(main_page_soup)
    discovered_metrics['ratings'] = extract_ratings(review_page_soup)
    # other metrics go here
    return Distro(distro_name, metrics=discovered_metrics)
