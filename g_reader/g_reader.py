#!/usr/bin/python
# -*- coding: utf-8 -*-
#
"""This file contains GReader class to get RSS information from Google Reader.

Copyleft rom.cpp@gmail.com
"""

import getpass
import urllib
import urllib2
from xml.dom import minidom


class GReader(object):
    """Class to get RSS information from Google Reader.

    Attributes:
        email: Google account email address
        passwd: password
        auth: Authrization token
        rsss: hash of RSS feeds
    """
    def __init__(self, email=None, passwd=None):
        self.email = email
        self.passwd = passwd

    def RequestAuth(self, email=None, passwd=None):
        """Request for authentication to connect reader service."""

        # Overwrite email and passwd.
        if email is not None:
            self.email = email
        if passwd is not None:
            self.passwd = passwd

        # Check for None values.
        if self.email is None:
            raise
        if self.passwd is None:
            self.passwd = getpass.getpass()
            if self.passwd is None:
                raise

        # Web request for authentication.
        url = 'https://www.google.com/accounts/ClientLogin'
        params = {
            'Email': self.email,
            'Passwd': self.passwd,
            'service': 'reader',
        }
        req = urllib2.Request(url, urllib.urlencode(params))
        try:
            resp = urllib2.urlopen(req)
        except urllib2.HTTPError, e:
            raise Exception('ClientLogin failed.')

        # Get auth.
        for line in resp:
            c = line.split('=', 1)
            if c[0] == 'Auth':
                self.auth = c[1]

    def RequestFeeds(self):
        """Request feed information and get feed list."""

        # Web request for feeds.
        url = 'https://www.google.com/reader/api/0/subscription/list'
        header = {'Authorization': 'GoogleLogin auth=' + self.auth}
        req = urllib2.Request(url, None, header)
        try:
            resp = urllib2.urlopen(req)
        except urllib2.HTTPError, e:
            raise Exception('Failed to connect Google Reader.')

        # Get feed ids and titles.
        xdoc = minidom.parse(resp)
        objects = xdoc.getElementsByTagName('object')
        self.rsss = {}
        for o in objects:
            rss = {'total': 0, 'starred': 0}
            for c in o.childNodes:
                if c.getAttribute('name') in ('id', 'title'):
                    rss[c.getAttribute('name')] = c.childNodes[0].data
            if 'id' in rss and 'title' in rss:
                self.rsss[rss['id']] = rss

    def RequestCounts(self):
        """Request read articles and count for each id."""

        # Number of sampling articles.
        num = 1000

        # Web request for read articles.
        url = ('https://www.google.com/reader/atom/user/-/state/com.google'
               '/read?n=' + str(num))
        header = {'Authorization': 'GoogleLogin auth=' + self.auth}
        req = urllib2.Request(url, None, header)
        try:
            resp = urllib2.urlopen(req)
        except urllib2.HTTPError, e:
            raise Exception('Failed to connect Google Reader.')

        # Count read and starred article for each id.
        xdoc = minidom.parse(resp)
        entries = xdoc.getElementsByTagName('entry')
        for e in entries:
            id = None
            star = 0
            for c in e.childNodes:
                if c.nodeName == 'source':
                    id = c.getAttribute('gr:stream-id')
                elif (c.nodeName == 'category' and
                        c.getAttribute('label') == 'starred'):
                    star = 1
            if id in self.rsss.keys():
                self.rsss[id]['total'] += 1
                self.rsss[id]['starred'] += star

    def GetIds(self):
        return self.rsss.keys()

    def GetTitle(self, id):
        return self.rsss[id]['title']

    def GetTotal(self, id):
        return self.rsss[id]['total']

    def GetStarred(self, id):
        return self.rsss[id]['starred']


if __name__ == '__main__':
    email = 'youremail@gmail.com'
    passwd = 'xxx'

    gr = GReader(email, passwd)
    gr.RequestAuth()
    gr.RequestFeeds()
    gr.RequestCounts()

    out = []
    val = {}
    for id in gr.GetIds():
        title = gr.GetTitle(id)
        total = gr.GetTotal(id)
        starred = gr.GetStarred(id)

        if total > 0:
            s = ("%6.1f %% : %2d / %2d : %s"
                 % (100.0 * starred / total, starred, total, title))
            out.append(s)
            val[s] = total - (1.0 * starred / total)

    out.sort(key=lambda x: val[x])
    out.reverse()
    for x in out:
        print x
