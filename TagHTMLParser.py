from HTMLParser import HTMLParser

'''
TagHTMLParser extends HTMLParser, and sets the following properties:

lines_info: a dictionary
    'key': line number
    'value': an ordered list of tuples (position, tagname) for each start tag on that line

tagcounts: a dictionary
    'key': tag name
    'value': num instances of tag name in html
'''
class TagHTMLParser(HTMLParser):
    lines_info, tagcounts = None, None

    def __init__(self):
        HTMLParser.__init__(self)
        self.lines_info = {}
        self.tagcounts = {}

    def handle_starttag(self, tag, attrs):
        pos = TagHTMLParser.getpos(self)
        if not pos[0] in self.lines_info:
            self.lines_info[pos[0]] = []
        self.lines_info[pos[0]].append((pos[1], tag))

        if tag in self.tagcounts:
            self.tagcounts[tag] += 1
        else:
            self.tagcounts[tag] = 1
