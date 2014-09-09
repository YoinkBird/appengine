import webapp2

# Content-Type = 'text/plain' # https://en.wikipedia.org/wiki/Web_Server_Gateway_Interface#Example_application
class MainPage(webapp2.RequestHandler):
  def get(self):
    self.response.headers['Content-Type'] = 'text/plain'
    self.response.write('Hello World!')

# debug = True    # print stack trace on errors
application = webapp2.WSGIApplication(
    [('/', MainPage),],
    debug = True)
