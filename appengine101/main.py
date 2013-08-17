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
import cgi
import urllib
import webapp2

from google.appengine.ext import ndb
from google.appengine.api import users

import jinja2
import os

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class Greeting(ndb.Model):
  """Models an individual guestbook entry with author, content, and date."""
  author = ndb.UserProperty()
  content = ndb.StringProperty()
  date = ndb.DateTimeProperty(auto_now_add=True)

  @classmethod
  def query_book(cls, ancestor_key):
    return cls.query(ancestor=ancestor_key).order(-cls.date)

class MainPage(webapp2.RequestHandler):
  def get(self):
    self.response.out.write('<html><body>')
    #self.response.out.write(self.request.environ)
    guestbook_name = self.request.get('guestbook_name')
    # There is no need to actually create the parent Book entity; we can
    # set it to be the parent of another entity without explicitly creating it
    ancestor_key = ndb.Key("Book", guestbook_name or "*notitle*")
    greetings = Greeting.query_book(ancestor_key).fetch(20)

    if users.get_current_user():
      url = users.create_logout_url(self.request.uri)
      url_linktext = 'Logout'
    else:
      url = users.create_login_url(self.request.uri)
      url_linktext = 'Login'

    template_values = {
      'greetings': greetings,
      'url': url,
      'url_linktext': url_linktext,
      'guestbook_name': guestbook_name

    }

    template = jinja_environment.get_template('index.html')
    self.response.out.write(template.render(template_values))

class Guestbook(webapp2.RequestHandler):
  def post(self):
    user = users.get_current_user()
    if user:
      content = self.request.get('content')
    else:
      content = 'From ' + self.request.environ['REMOTE_ADDR'] + ' ' + self.request.get('content')
    # Set parent key on each greeting to ensure that each
    # guestbook's greetings are in the same entity group.
    guestbook_name = self.request.get('guestbook_name')
    
    # There is no need to actually create the parent Book entity; we can
    # set it to be the parent of another entity without explicitly creating it
    greeting = Greeting(parent=ndb.Key("Book", guestbook_name or "*notitle*"),
                        content = content)
    if user:
      greeting.author = user

    greeting.put()
    self.redirect('/?' + urllib.urlencode({'guestbook_name': guestbook_name}))

app = webapp2.WSGIApplication([
  ('/', MainPage),
  ('/sign', Guestbook)
])
