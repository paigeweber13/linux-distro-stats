#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "Brian Weber"
__version__ = "0.1.0"
__license__ = "MIT"

# doesn't work right now... not sure why...?
# import distro

# third party imports
from bs4 import BeautifulSoup

import urllib.request

### CONSTANTS ###
reviewPageBaseUrl = "https://distrowatch.com/dwres.php?resource=ratings&distro="
# temp, will be replaced by text from a file
distrosToCheck = ["slackware"]
linuxDistros = []

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
    #         reviewPageBaseUrl + distro)
    # print(reviewPageHtml)
    # print(reviewPageHtml["slackware"].read())
    # return reviewPageHtml

def getReviewsPageHtml(distroName):
    reviewPageHtml = urllib.request.urlopen(reviewPageBaseUrl + distroName)
    return reviewPageHtml

def extractReviewText(reviewPageHtml):
    soup = BeautifulSoup(reviewPageHtml, "html.parser")
    reviewCells = soup.find_all(is_review_cell)
    reviewsText = ''
    for cell in reviewCells:
        cell.form.decompose()
        reviewsText += cell.text
        reviewsText += ' '
    reviewsText = reviewsText.replace('\n', ' ')
    reviewsText = reviewsText.replace('\r', ' ')
    reviewsText = reviewsText.replace('.', ' ')
    reviewsText = reviewsText.replace('(', ' ')
    reviewsText = reviewsText.replace(')', ' ')
    reviewsText = reviewsText.replace(',', ' ')
    reviewsText = reviewsText.replace('!', ' ')
    reviewsText = reviewsText.replace(',', ' ')

    # html = htmlDictionary['slackware'].read()
    # html = htmlDictionary['slackware']
    # soup = BeautifulSoup(html, "html.parser")
    # reviewText = soup.select('td[width="70%"]')

    return reviewsText

# main
def main():
    return extractReviewText(getReviewsPageHtml(distrosToCheck[0]))

if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
