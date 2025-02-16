import meeplib
import traceback
import cgi

#Updated for HW1 8:15 Jan16

def initialize():
    # create a default user
    u = meeplib.User('test', 'foo')

    # create a single message
    meeplib.Message('my title', 'This is my message!', u)

    # done.

class MeepExampleApp(object):
    """
WSGI app object.
"""
    def index(self, environ, start_response):
        start_response("200 OK", [('Content-type', 'text/html')])

        username = 'test'

        return ["""you are logged in as user: %s.<p><a href='/m/add'>Add a message</a><p><a href='/login'>Log in</a><p><a href='/logout'>Log out</a><p><a href='/m/list'>Show messages</a>""" % (username,)]

    def login(self, environ, start_response):
        # hard code the username for now; this should come from Web input!
        username = 'test'

        # retrieve user
        user = meeplib.get_user(username)

        # set content-type
        headers = [('Content-type', 'text/html')]
        
        # send back a redirect to '/'
        k = 'Location'
        v = '/'
        headers.append((k, v))
        start_response('302 Found', headers)
        
        return "no such content"

    def logout(self, environ, start_response):
        # does nothing
        headers = [('Content-type', 'text/html')]

        # send back a redirect to '/'
        k = 'Location'
        v = '/'
        headers.append((k, v))
        start_response('302 Found', headers)
        
        return "no such content"

    def list_messages(self, environ, start_response):
        messages = meeplib.get_all_messages()

        s = []
        for m in messages:
            s.append('id: %d<p>' % (m.id,))
            s.append('title: %s<p>' % (m.title))
            s.append('message: %s<p>' % (m.post))
            s.append('author: %s<p>' % (m.author.username))
            s.append('<form action="delete_action" method="POST"><input type="hidden" name="messageID" value="%d"><input type="submit" value="Delete Message"></form>' % (m.id))
            s.append('<hr>')
        s.append("<a href='../../'>index</a>")
            
        headers = [('Content-type', 'text/html')]
        start_response("200 OK", headers)
        
        return ["".join(s)]

    def add_message(self, environ, start_response):
        headers = [('Content-type', 'text/html')]
        
        start_response("200 OK", headers)

        return """<form action='add_action' method='POST'>Title: <input type='text' name='title'><br>Message:<input type='text' name='message'><br><input type='submit'></form>"""

    def add_message_action(self, environ, start_response):
        print environ['wsgi.input']
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)

        title = form['title'].value
        message = form['message'].value
        
        username = 'test'
        user = meeplib.get_user(username)
        
        new_message = meeplib.Message(title, message, user)

        headers = [('Content-type', 'text/html')]
        headers.append(('Location', '/m/list'))
        start_response("302 Found", headers)
        return ["message added"]

    def reply_to_mwssage(self, environ, start_response):
        print environ['wsgi.input']
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)
        parentID = form['id'].value;
        s = []
        start_response("200 OK", [('Content-type', 'text/html')])
        s.append("<p><p><a href = '../../'>Return to Index</a>")
        return "".join(s)
        
    def delete_action(self, environ, start_response):
        print environ['wsgi.input']
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)

        id = form['messageID'].value
        message = meeplib.get_message(int(id))
        meeplib.delete_message(message)
                     
        headers = [('Content-type', 'text/html')]
        headers.append(('Location', '/m/list'))
        start_response("302 Found", headers)
        return ["message deleted"]
        

        
    
    def __call__(self, environ, start_response):
        # store url/function matches in call_dict
        call_dict = { '/': self.index,
                      '/login': self.login,
                      '/logout': self.logout,
                      '/m/list': self.list_messages,
                      '/m/add': self.add_message,
                      '/m/add_action': self.add_message_action,
                      '/m/delete_action': self.delete_action
                      }

        # see if the URL is in 'call_dict'; if it is, call that function.
        url = environ['PATH_INFO']
        fn = call_dict.get(url)

        if fn is None:
            start_response("404 Not Found", [('Content-type', 'text/html')])
            return ["Page not found."]

        try:
            return fn(environ, start_response)
        except:
            tb = traceback.format_exc()
            x = "<h1>Error!</h1><pre>%s</pre>" % (tb,)

            status = '500 Internal Server Error'
            start_response(status, [('Content-type', 'text/html')])
            return [x]

        def print_messages(m, s, level):
            if(level != 0):
                s.append('<blockquote>')
                s.append('<hr>')
                s.append('id: %d<br/>' % (m.id,))
                s.append('title: %s<br/>' % (m.title))
                s.append('message: %s<br/>' % (m.post))
                s.append('author: %s<p>' % (m.author.username))
                s.append("""
                <form action="add" method="POST">
                <input type = 'submit' value = 'Reply'>
                <input type = 'hidden' name ='pID' value = %d>
                </form>""" % (m.id))
                s.append("""
                <form action = 'delete' method = 'POST'>
                <input type = 'submit' value = 'Delete Post'>
                <input type = 'hidden' name = 'id' value = '%d'>
                </form>""" % (m.id))

                if(m.replies != []):
                    for r in m.replies:
                        print_messages(meeplib.get_message(r), s, level + 1)
                        s.append('</blockquote>')
            
                return s
