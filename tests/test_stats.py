#!/usr/bin/env python3
""" tests stats functions

does NOT test getting html from the internet"""

import unittest
from datetime import date
from bs4 import BeautifulSoup

import context
import linuxstats.stats
import linuxstats.distro

# constants
TEST_DISTRIBUTION_NAME = 'fakenix'

class StatsTestCase(unittest.TestCase):
    """ standard unittest class. See
    https://docs.python.org/3/library/unittest.html """
    def setUp(self):
        #self.test_distro = Distro(TEST_DISTRIBUTION_NAME)
        #self.reviews_page_html = linuxstats.stats.get_reviews_page_html(
        #    self.test_distro.name)
        self.test_review_page_html = """
            <html>
                <head>
                    <title>
                        Fakenix Review Page
                    </title>
                </head>
            <body>
                <tr>
                    <td width="30%" style="border:0" valign="top">
                        <b>Version:</b> 14.2<br><b>Rating:</b>
                        10<br><b>Date:</b> 2018-08-10<br><b>Votes:</b>
                        17<br><br><br>
                    </td>
                    <td width="70%" style="border:0" valign="top">
                        This is my review text. Lorem ipsum dolor sit amet,\r
                        consectetur adipiscing elit! Vestibulum lacinia tortor
                        sed erat suscipit pharetra? Aliquam (tincidunt)\r
                        elementum dapibus. Quisque ut, vulputate, et nibh.
                        Duis ultricies a augue eu dictum...()?!,'.
                        <br><br><br>
                        <form>
                        </form>
                    </td>
                </tr>
                <tr>
                    <td width="30%" style="border:0" valign="top">
                        <b>Version:</b> current<br><b>Rating:</b>
                        10<br><b>Date:</b> 2018-08-01<br><b>Votes:</b>
                        5<br><br><br>
                    </td>
                    <td width="70%" style="border:0" valign="top">
                        This is a different review. Duis at tempor lectus. Sed at
                        aliquam lorem, vitae suscipit ex.  Praesent at lorem est.
                        Ut sagittis enim sollicitudin aliquet ullamcorper. In quis
                        velit nec metus tempus pellentesque.  Phasellus eget mauris
                        porta, vulputate ex nec, venenatis lorem.  Morbi vel
                        fringilla enim. Nulla at ante id dolor gravida porttitor ut
                        sodales odio. 
                        <br><br><br>
                        <form>
                        </form>
                    </td>
                </tr>
            </body>
            </html>
            """
        self.review_page_soup = BeautifulSoup(self.test_review_page_html, 'html.parser')
        #self.test_distro = linuxstats.distro.Distro(TEST_DISTRIBUTION_NAME)
        self.test_main_page_html = """
            <td class="TablesTitle">
                <a href="images/fakenix.png">
                    <img src="images/fakenix-small.png" border="0"
                    title="Fakenix Unix Linux" vspace="6" hspace="6"
                    align="right">
                </a>
                <b>
                    <a href="dwres.php?resource=popularity">Popularity (hits per
                    day)</a>:
                </b>
                12 months: <b>29</b> (313), 6 months: <b>29</b> (305), 3
                months: <b>21</b> (307), 4 weeks: <b>25</b> (353), 1 week:
                <b>36</b> (307)<br><br><b><a
                href="ratings/resource/link">Average visitor rating</a></b>:
                <b>9.4</b>/10 from <b>139</b> <a
                href="ratings/link/for/fakenix">review(s)</a>.<br><br>
            </td>
            """
        self.main_page_soup = BeautifulSoup(self.test_main_page_html,
            'html.parser')

    def test_is_review_cell(self):
        """ tests if our function to find cells that contain review text works
        self.review_page_soup.find_all('td') finds all td tags and returns an array of
        them. Using index one, we check to see if the second td tag is a review
        cell, which it is. This can be verified by checking the html above
        """
        cell = self.review_page_soup.find_all('td')[1]
        self.assertTrue(linuxstats.stats.is_review_cell(cell))

    def test_extract_review_text(self):
        """ tests if we can get multiple reviews and properly eliminate
        unnecessary whitespace and punctuation """
        expected_text = """ This is my review text Lorem ipsum dolor sit amet
                        consectetur adipiscing elit Vestibulum lacinia tortor
                        sed erat suscipit pharetra Aliquam  tincidunt elementum
                        dapibus Quisque ut  vulputate et nibh Duis ultricies a
                        augue eu dictum ' This is a different review Duis at
                        tempor lectus Sed at aliquam lorem vitae suscipit ex
                        Praesent at lorem est  Ut sagittis enim sollicitudin
                        aliquet ullamcorper In quis velit nec metus tempus
                        pellentesque  Phasellus eget mauris porta vulputate
                        ex nec venenatis lorem  Morbi vel fringilla enim
                        Nulla at ante id dolor gravida porttitor ut sodales
                        odio """
        expected_text = ' '.join(expected_text.split())
        actual_text = linuxstats.stats.extract_review_text(
            self.review_page_soup)
        print('text we got:')
        print(actual_text)
        print('text we expected:')
        print(expected_text)
        self.assertEqual(actual_text, expected_text)

    def test_is_rating_cell(self):
        """ tests if our function to find cells that contain ratings works
        """
        cell = self.review_page_soup.find_all('td')[0]
        self.assertTrue(linuxstats.stats.is_rating_cell(cell))

    def test_extract_ratings(self):
        expected_dict = {date(2018, 8, 10): 10, date(2018, 8, 1): 10}
        actual_dict = linuxstats.stats.extract_ratings(self.review_page_soup)
        print('expected dictionary:')
        print(expected_dict)
        print('actual dictionary:')
        print(actual_dict)
        self.assertEqual(actual_dict, expected_dict)

    def test_extract_popularity(self):
        expected_dict = {'1w':36, '4w':25, '3m':21, '6m':29, '12m':29}
        actual_dict = linuxstats.stats.extract_popularity(self.main_page_soup)
        print('expected dictionary:')
        print(expected_dict)
        print('actual dictionary:')
        print(actual_dict)
        self.assertEqual(actual_dict, expected_dict)

if __name__ == '__main__':
    unittest.main()
