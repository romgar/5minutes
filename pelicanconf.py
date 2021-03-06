#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = "Romain Garrigues"
SITENAME = "5minutes"
SITEURL = ""

PATH = "content"

TIMEZONE = "Europe/London"

DEFAULT_LANG = "en"

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (
    ("Pelican", "http://getpelican.com/"),
    ("Python.org", "http://python.org/"),
    ("Jinja2", "http://jinja.pocoo.org/"),
)

# Social widget
SOCIAL = (
    ("@jrmi", "https://twitter.com/jrmipp/"),
    ("@rgarrigues", "https://twitter.com/rgarrigues/"),
)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True
