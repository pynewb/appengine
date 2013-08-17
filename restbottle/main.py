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

import bottle
from bottle import response, route

#@route('/hello/<name>')
#def index(name='World'):
#    return bottle.template('<b>Hello {{name}}</b>!', name=name)

people = [{"_id": 1, "firstName": "Charles", "lastName": "Charlesworth"},
          {"_id": 2, "firstName": "Denise", "lastName": "Dentiste"},
          {"_id": 3, "firstName": "Ben", "lastName": "Benjamin"}]

@route('/people')
def getpeople():
    response.content_type = 'application/json; charset=utf-8'
    return json.dumps(people)
#    return {'people': people}

@route('/people/<id>')
def getpeople(id):
    y = [x for x in people if x['_id'] == int(id)]
    if len(y) > 0:
        person = y[0]
    else:
        person = {}

    response.content_type = 'application/json; charset=utf-8'
    return json.dumps(person)
#    return {'person': person}

bottle.run(server='gae', debug=True)
app = bottle.app()
