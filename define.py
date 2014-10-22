#!/usr/bin/python

from __future__ import print_function, division

import argparse
from urllib2 import urlopen, Request

import gtk
import webkit
import bs4


def main(words):
    def address(words):
        return "http://{subdomain}thefreedictionary.com/{word}".format(
            subdomain="idioms." if len(words) > 1 else "",
            word='+'.join(words)
        )

    data, = map(str, bs4.BeautifulSoup(
        urlopen(
            Request(
                url=address(
                    words
                ),
                headers={
                    'User-Agent': (
                        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:33.0) '
                        'Gecko/20100101 Firefox/33.0'
                    ),
                }
            )
        )
    ).find_all('div', id='MainTxt'))

    window = gtk.Window()
    window.connect("destroy", gtk.mainquit)
    webview = webkit.WebView()
    webview.load_html_string(data, "http://thefreedictionary.com")
    window.add(webview)
    window.show_all()
    gtk.main()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Show definition of the word')
    parser.add_argument('word', nargs='+')
    args = parser.parse_args()

    main(
        words=args.word
    )
