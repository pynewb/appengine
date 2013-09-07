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
import json

import webapp2

# This dict is the "database"
people = {1: {"_id": 1, "firstName": "Charles", "lastName": "Charlesworth"},
          2: {"_id": 2, "firstName": "Denise", "lastName": "Dentiste"},
          3: {"_id": 3, "firstName": "Ben", "lastName": "Benjamin"}};

max_id = 3

class GetPeopleHandler(webapp2.RequestHandler):
    def get(self):
        self.response.status = '200 OK'
        self.response.content_type = 'application/json'
        self.response.charset = 'utf-8'
        self.response.write(json.dumps(people.values()))

    def post(self):
        global max_id
        # TODO: specify encoding
        person = json.loads(self.request.body);
        # TODO: what to do if person already specifies _id
        max_id += 1
        id = max_id
        person['_id'] = id
        people[id] = person
        self.response.status = "204 No Content"

class GetPersonHandler(webapp2.RequestHandler):
    def get(self, id):
        id = int(id)
        try:
            person = people[id];
            self.response.status = "200 OK"
            self.response.content_type = 'application/json'
            self.response.charset = 'utf-8'
            self.response.write(json.dumps(person))
        except KeyError:
            self.response.status = "404 Not Found"

    def delete(self, id):
        id = int(id)
        try:
            del people[id];
            self.response.status = "204 No Content"
        except KeyError:
            self.response.status = "404 Not Found"

    def put(self, id):
        id = int(id)
        if id in people:
            # TODO: specify encoding
            person = json.loads(self.request.body);
            person['_id'] = id
            people[id] = person
            self.response.status = "204 No Content"
        else:
            self.response.status = "404 Not Found"

    def delete(self, id):
        y = [x for x in people if x['_id'] == int(id)]
        if len(y) > 0:
            person = y[0]
            people.remove(person)
            #set response code OK
        else:
            person = {}
            #set response code Not Found
        #self.response.content_type = 'application/json'
        #self.response.charset = 'utf-8'
        #self.response.write(json.dumps(person))

    def post(self, id):
        person = json.loads(self.request.body)
        for i in range(len(people)):
            if people[i]['_id'] == int(id):
                people[i] = person
                #set response code OK
                return
        #set response code Not Found
        
        #self.response.content_type = 'application/json'
        #self.response.charset = 'utf-8'
        #self.response.write(json.dumps(person))

    def put(self, id):
        for i in range(len(people)):
            if people[i]['_id'] == int(id):
                #set response code Already Exists
                return

        person = json.loads(self.request.body)
        people.append(person)
        #set response code OK
        #self.response.content_type = 'application/json'
        #self.response.charset = 'utf-8'
        #self.response.write(json.dumps(person))

app = webapp2.WSGIApplication([
    ('/people', GetPeopleHandler),
    (r'/people/(\d+)', GetPersonHandler)
], debug=True)
