import os, requests
from flask import Flask, jsonify, render_template, request
from TagHTMLParser import TagHTMLParser

app = Flask(__name__)
#app.debug = True

#### Routing ####

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/_parse_url')
def parse_url():
    try:
        urlinput = request.args.get('urlinput')
        r = requests.get(urlinput)

        content_headers = r.headers.get('Content-Type', '')
        # if the "content-type" header exists, verify this is an html response
        # Note: sometimes the content-type header is missing, but response is still html
        if not ("content-type" in r.headers and "text/html" in content_headers):
            raise ValueError("Content is not html")

        # If the assumed encoding (r.encoding) is not specified in the headers,
        # replace it with more accurate chardet based detection (r.apparent_encoding)
        # Note: r.apparent_encoding is expensive!
        if r.encoding not in content_headers:
            r.encoding = r.apparent_encoding

        html = r.text
        if not html:
            html = ""

        rawstrings = html.split("\n")

        parser = TagHTMLParser()
        parser.feed(html)

        return jsonify(result=render_template('summary.html', rawstrings=rawstrings, tagcounts=parser.tagcounts, lines_info=parser.lines_info))
    except ValueError, err:
        return jsonify_error("Invalid Input: "+ str(err))
    except Exception, err:
        return jsonify_error("Could not process url: " + str(err))

def jsonify_error(err_msg):
    return jsonify(error=err_msg)

##### Template Filters #####

@app.template_filter('string_slice')
def string_slice(s, start, end):
    if s and start >= 0 and end <= len(s):
        return s[start:end]
    return s

@app.template_filter('get_tag_uid')
def get_tag_uid(tag, tagdict):
    # return unique id for tag, based on position in tagdict.keys()
    if tagdict and (tag in tagdict):
        return "tagid-"+str(tagdict.keys().index(tag))
    return tag

@app.template_filter('get_taginfo_for_line')
def get_taginfo_for_line(lines_info, lindex):
    if lines_info and (lindex in lines_info):
        return lines_info[lindex]
    return []
