#!/usr/bin/env python3
""" tests stats functions 

does NOT test getting html from the internet"""

import unittest
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
        self.html_doc = """
            <html>
                <head>
                    <title>
                        Fakenix Review Page
                    </title>
                </head>
            <body>
                <td width="70%" style="border:0" valign="top">
                    This is my review text. Lorem ipsum dolor sit amet,\r
                    consectetur adipiscing elit! Vestibulum lacinia tortor sed
                    erat suscipit pharetra? Aliquam (tincidunt) elementum\r
                    dapibus. Quisque ut, vulputate, et nibh. Duis ultricies a
                    augue eu dictum...()?!,'.
                    <br><br><br>
                    <form>
                    </form>
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
            </body>
            </html>
            """
        self.soup = BeautifulSoup(self.html_doc, 'html.parser')
        #self.test_distro = linuxstats.distro.Distro(TEST_DISTRIBUTION_NAME)

    def test_is_review_cell(self):
        self.assertTrue(linuxstats.stats.is_review_cell(self.soup.td))

    def test_extract_review_text(self):
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
        actual_text = linuxstats.stats.extract_review_text(self.html_doc)
        print('text we got:')
        print(actual_text)
        print('text we expected:')
        print(expected_text)
        self.assertEquals(actual_text, expected_text)

if __name__ == '__main__':
    unittest.main()
