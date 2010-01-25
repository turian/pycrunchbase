#!/usr/bin/env python

"""
pycrunchbase
============

by Joseph Turian

Python methods to interact with the Crunchbase API v1.

Detailed documentation is available at:
    http://groups.google.com/group/crunchbase-api/web/api-v1-documentation.

We don't implement all API methods.

Code initially based upon the friendfeed API v1 implementation in Python
(Apache License, Version 2.0).
"""

import base64
import datetime
import time
import urllib
import urllib2

# We require a JSON parsing library. These seem to be the most popular.
try:
    import cjson
    parse_json = lambda s: cjson.decode(s.decode("utf-8"), True)
except ImportError:
    try:
        import simplejson
        parse_json = lambda s: simplejson.loads(s.decode("utf-8"))
    except ImportError:
        import json
        parse_json = lambda s: _unicodify(json.read(s))

#    def fetch_home_feed(self, **kwargs):
#        """Returns the entries the authenticated user sees on their home page.
#
#        Authentication is always required.
#        """
#        return self._fetch_feed("/api/feed/home", **kwargs)

def retrieve(namespace, permalink, **kwargs):
    """
    To retrieve information about a specific entity on CrunchBase.
     
    The available namespaces are:
     company
     person
     financial-organization 
     product
     service-provider

    <permalink> referrers to an entity's permalink as seen in the URL for its regular CrunchBase page.
      
    Also, you can append a callback query param to have the result passed
    to a callback method of your choice.
    """
    uri = "/%s/%s.js" % (namespace, permalink)
    return _fetch(uri, **kwargs)

def list(pluralnamespace, **kwargs):
    """
    List Entities

    To retrieve a list of all of the entities in a certain namespace on CrunchBase.
  
    The plural available namespaces are:
      companies
      people
      financial-organizations
      products
      service-providers
    This action does not support JavaScript callbacks.
    """
    uri = "/%s.js" % (pluralnamespace)
    return _fetch(uri, **kwargs)

def _fetch(uri, post_args=None, **url_args):
    url_args["format"] = "json"
    args = urllib.urlencode(url_args)
    url = "http://api.crunchbase.com/v/1" + uri + "?" + args
    if post_args is not None:
        request = urllib2.Request(url, urllib.urlencode(post_args))
    else:
        request = urllib2.Request(url)
    stream = urllib2.urlopen(request)
    data = stream.read()
    stream.close()
    return parse_json(data)

#def _parse_date(self, date_str):
#    rfc3339_date = "%Y-%m-%dT%H:%M:%SZ"
#    return datetime.datetime(*time.strptime(date_str, rfc3339_date)[:6])

def _unicodify(json):
    """Makes all strings in the given JSON-like structure unicode."""
    if isinstance(json, str):
        return json.decode("utf-8")
    elif isinstance(json, dict):
        for name in json:
            json[name] = _unicodify(json[name])
    elif isinstance(json, list):
        for part in json:
            _unicodify(part)
    return json


def _example():
    print retrieve("company", "facebook")
    print list("companies")

if __name__ == "__main__":
    _example()
