appengine
=========

Learning to Use AppEngine

On the question of using webapp[2] versus Bottle, Flask or others:

http://stackoverflow.com/questions/6774371/flask-vs-webapp2-for-google-app-engine

>>>
Disclaimer: I'm the author of tipfy and webapp2.

A big advantage of sticking with webapp (or its natural evolution, webapp2) is that you don't have to create your own versions for existing SDK handlers for your framework of your choice.

For example, deferred uses a webapp handler. To use it in a pure Flask view, using werkzeug.Request and werkzeug.Response, you'll need to implement deferred for it (like I did here for tipfy).

The same happens for other handlers: blobstore (Werkzeug still doesn't support range requests, so you'll need to use WebOb even if you create your own handler -- see tipfy.appengine.blobstore), mail, XMPP and so on, or others that are included in the SDK in the future.

And the same happens for libraries created with App Engine in mind, like ProtoRPC, which is based on webapp and would need a port or adapter to work with other frameworks, if you don't want to mix webapp and your-framework-of-choice handlers in the same app.

So, even if you choose a different framework, you'll end a) using webapp in some special cases or b) having to create and maintain your versions for specific SDK handlers or features, if you'll use them.

I much prefer Werkzeug over WebOb, but after over one year porting and maintaining versions of the SDK handlers that work natively with tipfy, I realized that this is a lost cause -- to support GAE for the long term, best is to stay close to webapp/WebOb. It makes support for SDK libraries a breeze, maintenance becomes a lot easier, it is more future-proof as new libraries and SDK features will work out of the box and there's the benefit of a large community working around the same App Engine tools.

A specific webapp2 defense is summarized here. Add to those that webapp2 can be used outside of App Engine and is easy to be customized to look like popular micro-frameworks and you have a good set of compelling reasons to go for it. Also, webapp2 has a big chance to be included in a future SDK release (this is extra-official, don't quote me :-) which will push it forward and bring new developers and contributions.

That said, I'm a big fan of Werkzeug and the Pocoo guys and borrowed a lot from Flask and others (web.py, Tornado), but -- and, you know, I'm biased -- the above webapp2 benefits should be taken into account.

share|improve this answer
edited Jul 22 '11 at 7:21

answered Jul 22 '11 at 7:07

moraes
5,2421731
<<<
