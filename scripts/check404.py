# check404.py
#
# A simple python script to check for broken links in HTML files. Largely based
# on my check404.sh program I wrote a while back, just ported to Python for
# maintainability and to use a higher level scripting language then bash.


import sys
if sys.version_info[0] < 3:
    # Python 2 specific imports
    from HTMLParser import HTMLParser
    import urlparse
else:
    # Python 3 specific imports
    from html.parser import HTMLParser
    from urllib.parse import urlparse
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import argparse
import re
import requests
import glob


# Terminal colors
#
# General use is like so:
# print(tcolors.BLUE + "This text is blue" + tcolors.END)
class tcolors:
    END_COLOR = '\033[0m'  # Remove all formatting to console output
    UNDERLINE = '\033[4m'  # Add underline to console output
    RED = '\033[91m'       # Turn console output red
    GREEN = '\033[92m'     # Turn console output green
    YELLOW = '\033[93m'    # Turn console output yellow
    BLUE = '\033[94m'      # Turn console output blue
    PURPLE = '\033[95m'    # Turn console output purple
    CYAN = '\033[96m'      # Turn console output cyan


# A simple HTML parser that prints color coded status codes to absolute URLs in
# <a> tags
class SimpleLinkParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if (tag == 'a'):
            for key, value in attrs:
                if (key == 'href'):
                    if (re.match(r'^https?:\/\/', value)):
                        res = requests.get(value, verify=False)

                        if (res.status_code >= 200 and res.status_code < 300):
                            # Success
                            print('{0}{1}{2} :: {3}'.format(tcolors.GREEN,
                                                            res.status_code,
                                                            tcolors.END_COLOR,
                                                            value))
                        elif (res.status_code >= 300 and
                              res.status_code < 400):
                            # Redirect
                            print('{0}{1}{2} :: {3}'.format(tcolors.YELLOW,
                                                            res.status_code,
                                                            tcolors.END_COLOR,
                                                            value))
                        elif (res.status_code >= 400 and
                              res.status_code < 500):
                            # Client Error
                            print('{0}{1}{2} :: {3}'.format(tcolors.RED,
                                                            res.status_code,
                                                            tcolors.END_COLOR,
                                                            value))
                        elif (res.status_code >= 500 and
                              res.status_code < 600):
                            # Server Error
                            print('{0}{1}{2} :: {3}'.format(tcolors.RED,
                                                            res.status_code,
                                                            tcolors.END_COLOR,
                                                            value))
                        else:
                            # Iunno man
                            print('{0}{1}{2} :: {3}'.format(tcolors.CYAN,
                                                            res.status_code,
                                                            tcolors.END_COLOR,
                                                            value))

    def handle_endtag(self, tag):
        pass

    def handle_data(self, data):
        pass


def main():
    app_description = ('A simple python script to test for broken links in '
                       'HTML files')
    # Get command-line Args
    parser = argparse.ArgumentParser(app_description)

    # Flags
    pass

    # Required Arguments
    parser.add_argument(
        'html_files',
        type=str,
        nargs='+',
        help='Path(s) to HTML files')

    args = parser.parse_args()

    link_parser = SimpleLinkParser()

    htmlfiles = args.html_files
    if (len(htmlfiles) == 1):
        htmlfiles = glob.glob(htmlfiles[0])

    for html_file in htmlfiles:
        try:
            f = open(html_file)
            contents = f.read()
            f.close()

            link_parser.feed(contents)
        except Exception as e:
            print('--- An Exception occured ---')
            print('Exception instance: {0}'.format(type(e)))
            print('Exception args: {0}'.format(e.args))
            print(e)


if __name__ == '__main__':
    main()
