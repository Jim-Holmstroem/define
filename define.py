#!/usr/bin/python

from __future__ import print_function, division

from functools import wraps
import argparse
import os
from urllib2 import urlopen, Request

import gtk
import webkit
import bs4


def main(
    words,
    cache_directory=os.path.join(
        os.path.expanduser('~'),
        '.define_cache',
    )
):

    def concatenate_words(words):
        return '+'.join(words)

    def cached(get_data):
        @wraps(get_data)
        def _cached(words):
            word = concatenate_words(words)
            cache_name = os.path.join(
                cache_directory,
                '{word}.htm'.format(word=word),
            )

            def save(data, word, cache_directory=cache_directory):
                try:
                    os.mkdir(cache_directory)
                except OSError as ose:
                    ose

                with open(cache_name, 'w') as f:
                    map(f.write, data)

                return data

            if os.path.isfile(cache_name):
                with open(cache_name) as f:
                    return (
                        '<div style='
                        '"position: fixed; bottom: 4px; right: 4px;">'
                        '[CACHED]'
                        '</div>'
                    ) + "\n".join(f)
            else:
                return save(
                    data=get_data(words),
                    word=word
                )

        return _cached

    def address(words):
        return "http://{subdomain}thefreedictionary.com/{word}".format(
            subdomain="idioms." if len(words) > 1 else "",
            word=concatenate_words(words)
        )

    data = cached(
        lambda words: str(bs4.BeautifulSoup(
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
        ).find_all('div', id='MainTxt')[0])
    )(words)

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
