from typing import Any, Optional

from lib.web import post


def pastebin(pastedata: str) -> Any:
    header = {"Content-Type": "application/json; charset=utf8"}
    # TODO move the following into configuration file when available
    dev_key = "redacted"
    username = "redacted"
    password = "redacted"
    privatepaste = 1 #limits for this are confusing http://192.184.83.59/SPG%20All/pastebin.com/faq.html#11a
    params = {
        "api_option": "paste",
        "api_user_key": "",
        "api_paste_private": privatepaste,
        "api_dev_key": dev_key,
        "api_paste_expire_date": "10M",
        "api_paste_format": "php",  # TODO sort out a valid list of formats
        "api_paste_code": pastedata
    }
    req = post(url="http://pastebin.com/api/api_post.php", data=params)
    if req.status == 200:
        return req.data
    else:
        return None

# fmt: off
def dpaste(pastedata: str, expiry_days: Optional[int] = 10, syntax: Optional[str] = "text") -> Any:
    valid_languages = [
        "coffee-script", "text", "tcl", "genshi", "csharp", "go",
        "trac-wiki", "lasso", "xml", "console", "fortran", "matlab", "ada", "erlang",
        "dpatch", "dart", "nginx", "python3", "bat", "lighty", "myghty", "d", "perl6",
        "js+erb", "fsharp", "cfm", "apacheconf", "tex", "modula2", "html+django", "scala",
        "applescript", "lua", "rb", "irc", "xslt", "js", "swift", "bash", "c", "vb.net",
        "ocaml", "jsp", "pytb", "clojure", "Clipper", "ragel", "smarty", "haskell",
        "puppet", "apl", "diff", "js+django", "rbcon", "pycon", "java", "yaml", "perl",
        "json", "common-lisp", "groff", "rhtml", "html+php", "python", "js+php", "factor",
        "rst", "groovy", "scheme", "bbcode", "objective-c", "dtd", "erb", "powershell",
        "rust", "prolog", "postscript", "as", "cobol", "ini", "io", "haml", "smalltalk",
        "mako", "py3tb", "make", "mathematica", "sourceslist", "html", "css", "llvm",
        "eiffel", "awk", "sql", "php", "scss", "dylan", "sparql", "sass", "django",
        "cpp", "delphi"
    ]
    if syntax not in valid_languages:
        syntax = "text"
    # TODO add dpaste_poster to configuration when available
    data = {
        "syntax": syntax,
        "expiry_days": expiry_days,
        "poster": "vicky",
        "content": pastedata
    }
    req = post(url="http://dpaste.com/api/v2/", data=data)
    if req.status == 201:
        return req.data.strip()
    else:
        return None
