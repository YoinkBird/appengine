from google.appengine.api import users
import webapp2

# Content-Type = 'text/plain' # https://en.wikipedia.org/wiki/Web_Server_Gateway_Interface#Example_application
class MainPage(webapp2.RequestHandler):
  def get(self):
    # checks for active google account session
    # If the user is already signed in to your application, get_current_user() returns the User object for the user.
    #  Otherwise, it returns None.
    user = users.get_current_user()

    if user:
      self.response.headers['Content-Type'] = 'text/plain'
      self.response.write('Hello , ' + user.nickname())
    else:
      # The redirect includes the URL to this page (self.request.uri) 
      #   so the Google account sign-in mechanism will send the user back here
      #   after the user has signed in or registered for a new account.
      self.redirect(users.create_login_url(self.request.uri))

# debug = True    # print stack trace on errors
application = webapp2.WSGIApplication(
    [('/', MainPage),],
    debug = True)
