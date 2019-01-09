#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2, datetime

from google.appengine.api import users
from google.appengine.ext import ndb


class SortenedUrls(ndb.Model):
    real_url = ndb.StringProperty()
    short_url = ndb.StringProperty()


class UrlsForUser(ndb.Model):
    email = ndb.StringProperty()
    short_url = ndb.StringProperty()


class UrlAnalytics(ndb.Model):
    short_url = ndb.StringProperty()
    visited_on = ndb.StringProperty()
    # client_ip = ndb.StringProperty()

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Created the new record')


class ShortUrlHandler(webapp2.RequestHandler):
    def get(self):
        surl = self.request.url
        obj = SortenedUrls.query(
            SortenedUrls.short_url == surl).fetch()
        if obj:
            self.redirect(str(obj[0].real_url), True)

        ua = UrlAnalytics()
        ua.short_url = surl
        ua.visited_on = str(datetime.datetime.now())
        # if self.request.client_addr():
        #     ua.client_ip = self.request.client_addr()
        # else:
        #     ua.client_ip = "NOT AVAILABLE"
        ua.put()


class UrlShortenHandler(webapp2.RequestHandler):

    def shorten(self, url):
        return self.request.host_url + "/" + str(id(url))

    def get(self):
        real_url = self.request.params["url"]
        if real_url:
            # Create the Short URL instance
            surl = SortenedUrls()
            surl.real_url = real_url
            surl.short_url = self.shorten(real_url)

            # Create user's item for short urls
            u4u = UrlsForUser()
            u4u.short_url = surl.short_url
            u4u.email = users.get_current_user().email()

            # Save the data into datastore
            surl.put()
            u4u.put()

            self.response.write("Short URL is: " + surl.short_url)




app = webapp2.WSGIApplication([
    ('/shorten', UrlShortenHandler),
    ('/.*', ShortUrlHandler)
], debug=True)
