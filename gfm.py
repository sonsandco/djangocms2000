"""
Github flavoured markdown - ported from
http://github.github.com/github-flavored-markdown/

Usage:

    html_text = markdown(gfm(markdown_text))

(ie, this filter should be run on the markdown-formatted string BEFORE the markdown
filter itself.)

"""

import hashlib, re

def gfm(text):

    
    # Extract pre blocks
    extractions = {}
    def pre_extraction_callback(matchobj):
        sha1 = hashlib.sha1(matchobj.group(0)).hexdigest()
        extractions[sha1] = matchobj.group(0)
        return "{gfm-extraction-%s}" % sha1
    text = re.sub(re.compile(r'<pre>.*?</pre>', re.MULTILINE | re.DOTALL), pre_extraction_callback, text)
     
     
    # prevent foo_bar_baz from ending up with an italic word in the middle
    def italic_callback(matchobj):
        if len(re.sub(r'[^_]', '', matchobj.group(0))) > 1:
            return matchobj.group(0).replace('_', '\_')
        else:
            return matchobj.group(0)
    text = re.sub(r'(?! {4}|\t)\w+_\w+_\w[\w_]*', italic_callback, text)
        
    
    # in very clear cases, let newlines become <br /> tags
    def newline_callback(matchobj):
        if len(matchobj.group(1)) == 1:
            return matchobj.group(0).rstrip() + '  \n'
        else:
            return matchobj.group(0)
    text = re.sub(r'^[\w\<][^\n]*(\n+)', newline_callback, text)
    
       
    # Insert pre block extractions
    def pre_insert_callback(matchobj):
        return extractions[matchobj.group(1)]
    text = re.sub(r'{gfm-extraction-([0-9a-f]{40})\}', pre_insert_callback, text)
         
    return text
