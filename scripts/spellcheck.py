# spellcheck.py
#
# A simply python script to spellcheck data in HTML files.


import sys
if sys.version_info[0] < 3:
    # Python 2 specific imports
    from HTMLParser import HTMLParser
    import urlparse
else:
    # Python 3 specific imports
    from html.parser import HTMLParser
    from urllib.parse import urlparse
import argparse
import re
import string
import glob


# A simple HTML parser to spell check words in between tags
class SpellCheckParser(HTMLParser):
    def __init__(self, wlst):
        HTMLParser.__init__(self)

        self.word_list = wlst
        self.file_name = ''
        self.curr_tag = []
        self.misspell_msg = ('Found a possibly misspelled word {0} in {1} '
                             'starting on line {2} from tag <{3}>')

    def handle_starttag(self, tag, attrs):
        self.curr_tag.append(tag)

    def handle_endtag(self, tag):
        self.curr_tag.pop()

    def handle_data(self, data):
        if (len(self.curr_tag) > 0 and self.curr_tag[-1] != 'script'):
            for word in data.split():
                word = word.lower()
                word = re.sub(r'\s+', '', word, flags=re.UNICODE)
                word = self.simple_punctuation_strip(word)
                if (not self.is_special(word) and word not in self.word_list):
                    print(self.misspell_msg.format(word, self.file_name,
                                                   self.getpos()[0],
                                                   self.curr_tag[-1]))

    def is_special(self, s):
        if (len(s) == 0):
            return True
        elif (re.match(r'^https?:\/\/', s)):
            return True
        elif (s.startswith('1st') or s.startswith('2nd') or
              s.startswith('3rd') or re.match(r'^\d+th$', s)):
            return True
        elif (re.match(r'^[\w.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', s)):
            return True

        return False


    def simple_punctuation_strip(self, s):
        while (len(s) > 0 and s[0] in string.punctuation):
            s = s[1:]
        while (len(s) > 0 and s[-1] in string.punctuation):
            s = s[:-1]

        return s

    def set_name(self, name):
        self.file_name = name


def main():
    app_description = 'A simple python script to spell check HTML files'

    # Get command-line args
    parser = argparse.ArgumentParser(app_description)

    # Flags
    parser.add_argument(
        '-w',
        '--word_lists',
        type=str,
        nargs='+',
        required=True,
        action='append',
        help='Path(s) to the wordlist(s)')

    # Required Arguments
    parser.add_argument(
        'html_files',
        type=str,
        nargs='+',
        help='Path(s) to html files')

    args = parser.parse_args()
    words = set()

    wordlists = args.word_lists
    if (len(wordlists) == 1 and len(wordlists[0]) == 1):
        wordlists = glob.glob(wordlists[0][0])

    for wlst in wordlists:
        try:
            f = open(wlst)

            for line in f.readlines():
                words.add(line.lower().strip())

            f.close()
        except Exception as e:
            print('--- An Exception occured in {0} ---'.format(wlst))
            print('Exception instance: {0}'.format(type(e)))
            print('Exception args: {0}'.format(e.args))
            print(e)

    spell_parser = SpellCheckParser(words)

    htmlfiles = args.html_files
    if (len(htmlfiles) == 1):
        htmlfiles = glob.glob(htmlfiles[0])

    for html_file in htmlfiles:
        spell_parser.set_name(html_file)
        try:
            f = open(html_file)
            contents = f.read()
            f.close()

            spell_parser.feed(contents)
            spell_parser.reset()
        except Exception as e:
            print('--- An Exception occured in {0} ---'.format(html_file))
            print('Exception instance: {0}'.format(type(e)))
            print('Exception args: {0}'.format(e.args))
            print(e)


if __name__ == '__main__':
    main()
