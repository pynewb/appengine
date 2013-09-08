//
//    Learning to use knockout
//    Copyright (C) 2013  pynewb
//
//    This program is free software; you can redistribute it and/or modify
//    it under the terms of the GNU General Public License as published by
//    the Free Software Foundation; either version 2 of the License, or
//    (at your option) any later version.
//
//    This program is distributed in the hope that it will be useful,
//    but WITHOUT ANY WARRANTY; without even the implied warranty of
//    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//    GNU General Public License for more details.
//
//    You should have received a copy of the GNU General Public License along
//    with this program; if not, write to the Free Software Foundation, Inc.,
//    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
//
var express = require('express');
var mongo = require('mongodb');
var BSON = mongo.BSONPure;

var app = express();
app.use(express.logger());
app.use(express.static(__dirname + "/public"));
app.use(express.bodyParser());

var server = new mongo.Server('localhost', 27017, {auto_reconnect: true});
var mongoClient = new mongo.MongoClient(server);
mongoClient.open(function(err, mongoClient) {
  if (err) {
    console.log('Error connecting to MongoDB: ' + err);
  } else {
    appDb = mongoClient.db("app");
    console.log("Connected to 'app' database");
    appDb.collection('people', {strict:true}, function (err, collection) {
      if (err) {
        console.log("The 'people' collection doesn't exist. Creating it with sample data...");
        populateDB();
      }
    });
  }
});

app.get('/people', function (req, res) {
  console.log("get /people");
    
  appDb.collection('people', function (err, collection) {
    collection.find().toArray(function (err, people) {
      if (err) {
        res.send({'error': 'An error has occurred - ' + err});
      } else {
        console.log('got people ' + JSON.stringify(people));        
        res.jsonp(people);  // N.B. support JSONP
      }
    });
  });
});

app.get('/people/:id', function (req, res) {
  console.log("get /people/" + req.params.id);
    
  appDb.collection('people', function (err, collection) {
    collection.findOne({'_id': new BSON.ObjectID(req.params.id)}, function (err, person) {
      if (err) {
        res.send({'error': 'An error has occurred - ' + err});
      } else {
        console.log('got person ' + JSON.stringify(person));
        res.jsonp(person);  // N.B. support JSONP
      }
    });
  });
});

app.delete('/people/:id', function (req, res) {
  console.log("delete /people/" + req.params.id);
    
  appDb.collection('people', function(err, collection) {
    collection.remove({'_id': new BSON.ObjectID(req.params.id)}, {safe: true}, function (err, result) {
      if (err) {
        res.send({'error': 'An error has occurred - ' + err});
      } else {
        console.log('' + result + ' document(s) deleted');
        res.send(req.body);
      }
    });
  });
});

app.post('/people', function (req, res) {
  // N.B. the caller can include _id
  console.log("post /people " + JSON.stringify(req.body));

  appDb.collection('people', function (err, collection) {
    collection.insert(req.body, {safe: true}, function (err, result) {
      if (err) {
        res.send({'error': 'An error has occurred - ' + err});
      } else {
        console.log('Success: ' + JSON.stringify(result[0]));
        res.send(result[0]);
      }
    });
  });
});

app.put('/people/:id', function (req, res) {
  var personWithoutId = JSON.parse(JSON.stringify(req.body));
  if (personWithoutId._id) {
    delete(personWithoutId._id);
  }
  console.log("put /people/" + req.params.id + " " + JSON.stringify(personWithoutId));
    
  appDb.collection('people', function(err, collection) {
    collection.update({'_id': new BSON.ObjectID(req.params.id)}, personWithoutId, {safe: true}, function (err, result) {
      if (err) {
        res.send({'error': 'An error has occurred - ' + err});
      } else {
        console.log('' + result + ' document(s) updated');
        res.send(req.body);
      }
    });
  });
});

/*--------------------------------------------------------------------------------------------------------------------*/
// Populate database with sample data -- Only used once: the first time the application is started.
// You'd typically not find this code in a real-life app, since the database would already exist.
var populateDB = function () {
 
  var people = [
    { firstName: 'Bert', lastName: 'Bertington' },
    { firstName: 'Charles', lastName: 'Charlesforth' },
    { firstName: 'Denise', lastName: 'Dentiste' }        
  ];

  appDb.collection('people', function(err, collection) {
    if (err) {
      console.log("Unable to connect to collection 'people' to populate it");
    } else {
      collection.insert(people, {safe:true}, function (err, result) {
      });
    }
  }); 
};

var port = process.env.PORT || 4730
app.listen(port);
console.log("listening on port " + port);
