#!/usr/bin/env python
#
# Copyright 2013 pynewb
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
import json

from google.appengine.ext import ndb

import webapp2

def get_parent_key():
    return ndb.Key('root', 'resttest')

class Person(ndb.Model):
    firstName = ndb.StringProperty()
    lastName = ndb.StringProperty()

    def to_dict(self):
        return {'key': self.key.urlsafe(), 'firstName': self.firstName, 'lastName': self.lastName}

    @classmethod
    def from_dict(cls, d):
        if 'key' in d:
            return cls(key=ndb.Key(urlsafe=d['key']), firstName=d['firstName'], lastName=d['lastName'])

        return cls(parent=get_parent_key(), firstName=d['firstName'], lastName=d['lastName'])

class GetPeopleHandler(webapp2.RequestHandler):
    def get_people(self):
        persons = Person.query(ancestor=get_parent_key())
        people = []
        for person in persons:
            people.append(person.to_dict())
            
        if len(people) == 0:
            # initialize the data store
            person = Person(parent=get_parent_key(), firstName='Charles', lastName='Charlesworth')
            person.put()
            person = Person(parent=get_parent_key(), firstName='Denise', lastName='Dentiste')
            person.put()
            person = Person(parent=get_parent_key(), firstName='Ben', lastName='Benjamin')
            person.put()

            persons = Person.query(ancestor=get_parent_key())
            for person in persons:
                people.append(person.to_dict())

        return people

    def get(self):
        people = self.get_people()
        self.response.status = '200 OK'
        self.response.content_type = 'application/json'
        self.response.charset = 'utf-8'
        self.response.write(json.dumps(people))

    def post(self):
        # TODO: specify encoding
        post_person = json.loads(self.request.body)
        person = Person.from_dict(post_person)
        person.put()
        self.response.status = "204 No Content"

class GetPersonHandler(webapp2.RequestHandler):
    def get(self, id):
        try:
            key = ndb.Key(urlsafe=id)
            person = key.get()
            self.response.status = "200 OK"
            self.response.content_type = 'application/json'
            self.response.charset = 'utf-8'
            self.response.write(json.dumps(person.to_dict()))
        except:
            self.response.status = "404 Not Found"

    def delete(self, id):
        try:
            key = ndb.Key(urlsafe=id)
            key.delete();
            self.response.status = "204 No Content"
        except KeyError:
            self.response.status = "404 Not Found"

    def put(self, id):
        try:
            key = ndb.Key(urlsafe=id)
            person = key.get()
            # TODO: specify encoding
            put_person = json.loads(self.request.body);
            person.populate(firstName=put_person['firstName'], lastName=put_person['lastName'])
            person.put()
            self.response.status = "204 No Content"
        except:
            self.response.status = "404 Not Found"

app = webapp2.WSGIApplication([
    ('/people', GetPeopleHandler),
    (r'/people/([^\\]+)', GetPersonHandler)
], debug=True)
