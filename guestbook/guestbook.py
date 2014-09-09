import cgi
import urllib
from google.appengine.api import users
from google.appengine.ext import ndb
import webapp2

MAIN_PAGE_FOOTER_TEMPLATE = """\
    <form action="/sign?%s" method="post">
      <div>
        <textarea name="content" rows="3" cols="60"></textarea>
      </div>
      <hr />
      <form>Guestbook name:
        <input value="%s" name="guestbook_name" />
        <input type="submit" value="switch" />
    </form>
    <a href="%s">%s</a>
  </body>
</html>
"""

DEFAULT_GUESTBOOK_NAME = 'default_guestbook'

# We set a parent key on the 'Greetings' to ensure that they are all in the same entity group.
# Queries across the single entity group will be consistent.
# However, the write rate should be limited to ~1/second.

def guestbook_key(guestbook_name=DEFAULT_GUESTBOOK_NAME):
  """Constructs a Datastore key for a Guestbook entity with guestbook_name."""
  return ndb.Key('Guestbook',guestbook_name)

class Greeting(ndb.Model):
  """Models an individual Guestbook entry."""
  author  = ndb.UserProperty()
  content = ndb.StringProperty(indexed=False)
  date    = ndb.DateTimeProperty(auto_now_add=True)

class MainPage(webapp2.RequestHandler):
  def get(self):
    outStr = '<html><body>'
    guestbook_name = self.request.get('guestbook_name',DEFAULT_GUESTBOOK_NAME)

    # Ancestor Queries, as shown here, are strongly consistent with the High Replication Datastore
    # Queries that span entity groups  are eventually consistent.
    # If we omitted the ancestor from this query there would be a slight chance
    #  that 'Greeting' that had just been written would not show up in a query.
    greetings_query = Greeting.query(
        ancestor = guestbook_key(guestbook_name)).order(-Greeting.date)
    greetings = greetings_query.fetch(10)

    msgTableStr = ""
    for greeting in greetings:
      msgTrStr = ""
      if greeting.author:
        msgTrStr += '<b>%s</b> wrote:' % greeting.author.nickname()
      else:
        msgTrStr += '<b>%s</b> wrote:' % 'Anonymous'
      msgTrStr = '  <tr>\n    <td>%s</td>' % msgTrStr
      msgTrStr += '<td><blockquote>%s</blockquote>' % cgi.escape(greeting.content)
      msgTrStr += '    </td>\n  </tr>\n'
      msgTableStr += msgTrStr
      #msgTableStr += '<blockquote>%s</blockquote>' % cgi.escape(greeting.content)
    if(msgTableStr != ""):
      msgTableStr = '<table border="1" cellspacing="0">\n%s</table>' % msgTableStr

    # append greetings for printing
    outStr += "\n<p>Current Messages:</p>"
    outStr += "\n%s\n" % msgTableStr

    if users.get_current_user():
      url = users.create_logout_url(self.request.uri)
      url_linktext = 'Logout'
    else:
      url = users.create_login_url(self.request.uri)
      url_linktext = 'Login'

    # Write the submission form and the footer of the page
    sign_query_params = urllib.urlencode({'guestbook_name': guestbook_name})

    outStr += '<hr />\n'
    outStr += '<p>Add an entry:</p>\n'
      # note: do not split this over several lines
    outStr += MAIN_PAGE_FOOTER_TEMPLATE % (sign_query_params, cgi.escape(guestbook_name), url, url_linktext)
    self.response.write(outStr)

    # from tutorial:
    #self.response.write(MAIN_PAGE_FOOTER_TEMPLATE % 
              #(sign_query_params, cgi.escape(guestbook_name), url, url_linktext))

class Guestbook(webapp2.RequestHandler):
  def post(self):
    # We set the same parent key on the 'Greeting' to ensure each Greeting is in the same entity group.
    # Queries across the single entity group will be consistent.
    # However, the write rate to a single entity group should be limited to ~1/second.
    guestbook_name = self.request.get('guestbook_name', DEFAULT_GUESTBOOK_NAME)
    greeting = Greeting(parent=guestbook_key(guestbook_name))

    if users.get_current_user():
      greeting.author = users.get_current_user()

    greeting.content = self.request.get('content')
    greeting.put()

    query_params = {'guestbook_name':guestbook_name}
    self.redirect('/?' + urllib.urlencode(query_params))

application = webapp2.WSGIApplication(
    [
      ('/', MainPage),
      ('/sign', Guestbook),
    ],
    debug = True)


# NOTES:
# Content-Type = 'text/plain' # https://en.wikipedia.org/wiki/Web_Server_Gateway_Interface#Example_application
