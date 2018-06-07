#!/usr/bin/env python3
"""
Module Docstring
"""

__author__ = "Brian Weber"
__version__ = "0.1.0"
__license__ = "MIT"

from bs4 import BeautifulSoup

import urllib.request

# constants
reviewPageBaseUrl = "https://distrowatch.com/dwres.php?resource=ratings&distro="

# temp, will be replaced by text from a file
distrosToCheck = ["slackware"]

# functions
def getReviewsPagesHtml(distroNames):
    """ gets html for distrowatch.com review pages for a list of linux distros

    arguments:
    distroNames -- a list of distribution names, with the spelling and
                   capitalization used in distrowatch.com links
    
    return value: a dictionary where keys are distro names and values are
                  httpResponse objects
    """
    
    reviewPageHtml = {}
    for distro in distroNames:
        reviewPageHtml[distro] = urllib.request.urlopen(
            reviewPageBaseUrl + distro)
    # print(reviewPageHtml)
    # print(reviewPageHtml["slackware"].read())
    return reviewPageHtml

def extractReviewText(htmlArray):
    """ given a list of httpresponse objects, extracts distrowatch review text, if any.

    arguments:
    htmlArray -- a list of httpResponse objects retrieved from distrowatch.com
                 review pages.

    return value: a dictionary where distro names are the keys and review text
                  are the values
    """
    html = htmlArray['slackware'].read()
    soup = BeautifulSoup(html, "html.parser")
    soup.select('td[width="70%"]')


# main
# def main():
#     """ Main entry point of the app """
#     print("""hello world! This is the python implementation of the
#         linux-distro-stats tool.""")


if __name__ == "__main__":
    """ This is executed when run from the command line """
    # main()
    extractReviewText(getReviewsPagesHtml(distrosToCheck))
