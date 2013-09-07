import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'])

DEFAULT_GUESTBOOK_NAME = 'default_guestbook'

class Guestbook(ndb.Model):
    date = ndb.DateTimeProperty(auto_now_add=True)

class Greeting(ndb.Model):
    """Models an individual Guestbook entry with author, content, and date."""
    author = ndb.UserProperty()
    content = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)


class MainHandler(webapp2.RequestHandler):

    def get(self):
        guestbook_name = self.request.get('guestbook_name',
                                          DEFAULT_GUESTBOOK_NAME)
        guestbook = Guestbook.get_or_insert(guestbook_name)
        greetings_query = Greeting.query(
            ancestor=guestbook.key).order(-Greeting.date)
        greetings = greetings_query.fetch(10)

        guestbook_query = Guestbook.query().order(-Guestbook.date)
#        guestbook_names = [urllib.quote_plus(gb.key.id()) for gb in guestbook_query.fetch(10)]
        guestbook_names = [gb.key.id() for gb in guestbook_query.fetch(10)]

        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'greetings': greetings,
            'guestbook_name': urllib.quote_plus(guestbook_name),
            'guestbook_names': guestbook_names,
            'url': url,
            'url_linktext': url_linktext,
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))

class GuestbookHandler(webapp2.RequestHandler):

    def post(self):
        # We set the same parent key on the 'Greeting' to ensure each Greeting
        # is in the same entity group. Queries across the single entity group
        # will be consistent. However, the write rate to a single entity group
        # should be limited to ~1/second.
        guestbook_name = self.request.get('guestbook_name',
                                          DEFAULT_GUESTBOOK_NAME)
        guestbook = Guestbook.get_or_insert(guestbook_name)

        greeting = Greeting(parent=guestbook.key)

        if users.get_current_user():
            greeting.author = users.get_current_user()

        greeting.content = self.request.get('content')
        greeting.put()

        query_params = {'guestbook_name': guestbook_name}
        self.redirect('/?' + urllib.urlencode(query_params))


application = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/sign', GuestbookHandler),
], debug=True)