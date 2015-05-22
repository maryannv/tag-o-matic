# tag-o-matic
Tag-o-matic examines the html for any url, and displays the tag counts and html source. It highlights selected opening tags in the source view. 

https://secure-brushlands-5655.herokuapp.com/

Overview
- Built using Flask. 
- Uses [requests](https://requests.readthedocs.org/en/v1.1.0/api/index.html) library to fetch and decode html content. 
- Uses [HTMLParser](https://docs.python.org/2/library/htmlparser.html) to find indexes of all start tags in the html source. During parsing, also builds a dictionary of tags to counts.
- The source is displayed by surrounding the content with <span> tags. Opening tags are placed in their own spans with a css class unique to that tag. This allows easy highlight toggling of all such spans using a jQuery selector.


Code of interest is in: tag_app.py, TagHTMLParser.py, templates/..., static/...

Design note:
- Only highlights opening tags, so that the number of highlights matches the tag counts.
