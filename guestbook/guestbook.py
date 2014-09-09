import cgi
from google.appengine.api import users
import webapp2

MAIN_PAGE_HTML = """\
<html>
  <body>
    <form action="/sign" method="post">
      <div>
        <textarea name="content" rows="3" cols="60"></textarea>
      </div>
      <div>
        <input type="submit" value="Sign Guestbook" />
      </div>
    </form>
  </body>
</html>
"""

class MainPage(webapp2.RequestHandler):
  def get(self):
    self.response.write(MAIN_PAGE_HTML)

class Guestbook(webapp2.RequestHandler):
  def post(self):
    writeStr = '<html><body>'
    writeStr += 'You wrote:'
    writeStr += '<pre>'
    writeStr += cgi.escape(self.request.get('content'))
    writeStr += '</pre>'
    writeStr += '</body></html>'

    self.response.write(writeStr)

# debug = True    # print stack trace on errors
application = webapp2.WSGIApplication(
    [
      ('/', MainPage),
      ('/sign', Guestbook),
    ],
    debug = True)


# NOTES:
# Content-Type = 'text/plain' # https://en.wikipedia.org/wiki/Web_Server_Gateway_Interface#Example_application
