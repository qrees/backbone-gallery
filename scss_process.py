import tempfile
import urlparse
import os
import re
import sys

__author__ = 'qrees'


TMP_FILE_PREFIX = os.path.join(tempfile.gettempdir(), tempfile.gettempprefix())

def _is_temp_file(filename):
    return filename.startswith(TMP_FILE_PREFIX)

if len(sys.argv) < 3:
    raise Exception("No input or output file given.")

CSS_IMPORT_RE = re.compile(ur"""@import \s+
    (?:url\()? #optional
    ["'] #begin-quote
    ([a-zA-Z0-9/_.-]+) # path
    ["'] #end-quote
    (?:\))? # end of url()
    ; #end of statement
""", re.UNICODE | re.VERBOSE)

def get_css_imports(path):
    imports = []

    base_dir = os.path.dirname(path)
    with open(media_root(path), "rb") as f:
        for line in f:
            if not line.strip():
                continue
            if not line.startswith('@'):
                continue
            match = CSS_IMPORT_RE.match(line)
            if match is None:
                continue
            imports.append(os.path.join(base_dir, match.group(1)))

    return imports

def css_follow_imports(filenames):
    # reverse makes this an efficient stack
    in_queue = [ (x, False) for x in reversed(filenames)]
    out_queue = []

    while in_queue:
        filename, visited = in_queue.pop()
        if not visited:
            in_queue.append((filename, True))
            imports = get_css_imports(filename)
            in_queue.extend((x, False) for x in imports) # follow imports
        else:
            out_queue.insert(0, filename)

    return out_queue

def media_root(filename):
    """
    Return the full path to ``filename``. ``filename`` is a relative path name in MEDIA_ROOT
    """
    if os.path.exists(filename):
        return filename
    dir, file = os.path.split(filename)
    filename1 = os.path.join(dir, '_%s.scss' % file)
    if os.path.exists(filename1):
        return filename1
    raise Exception("file %s not found" % filename)

def read_resource_file(filename):

    with open(media_root(filename), "rb") as input:
        data = input.read()
    return (u"\n// IMPORT:: %s \n" % (filename if not _is_temp_file(filename) else '[TEMP FILE]')).encode('utf-8') + data


def concat(filenames, separator=''):
    """
    Concatenate the files from the list of the ``filenames``, output separated with ``separator``.
    """
    r = ''
    out_queue = css_follow_imports(filenames)

    for filename in out_queue:
        r += read_resource_file(filename)
        r += separator

    return r

from scss import Scss

options = '''
@option compress: no;
'''

def process(file):
    output = options
    output += concat([file])
    css = Scss()
    with open(sys.argv[2], "w") as file:
        file.write(css.compile(output))


process(sys.argv[1])
