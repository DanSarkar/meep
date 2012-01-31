
__all__ = ['Message', 'get_all_messages', 'get_message', 'delete_message',
           'User', 'get_user', 'get_all_users', 'delete_user']

###
# internal data structures & functions; please don't access these
# directly from outside the module. Note, I'm not responsible for
# what happens to you if you do access them directly. CTB

# a dictionary, storing all messages by a (unique, int) ID -> Message object.
_messages = {}

def _get_next_message_id():
    if _messages:
        return max(_messages.keys()) + 1
    return 0

# a dictionary, storing all users by a (unique, int) ID -> User object.
_user_ids = {}

# a dictionary, storing all users by username
_users = {}

def _get_next_user_id():
    if _users:
        return max(_user_ids.keys()) + 1
    return 0
    
def _get_next_user_id_ORG():
    if _users:
        return max(_users.keys()) + 1
    return 0

def _reset():
    """
Clean out all persistent data structures, for testing purposes.
"""
    global _messages, _users, _user_ids
    _messages = {}
    _users = {}
    _user_ids = {}

###

class Message(object):
    """
Simple "Message" object, containing title/post/author.

'author' must be an object of type 'User'.

"""
    def __init__(self, title, post, author, is_reply = False):
        self.replies = {}
        self.title = title
        self.post = post

        assert isinstance(author, User)
        self.author = author

        if is_reply == False:
            self._save_message()

    def _save_message(self):
        self.id = _get_next_message_id()

        # register this new message with the messages list:
        _messages[self.id] = self

    def add_reply(self, newMessage):
     newId = 0
     if self.replies:
            newId = max(self.replies.keys()) + 1
        self.replies[newId] = newMessage

    def get_replies(self):
        return self.replies.values()

def get_all_messages(sort_by='id'):
    return _messages.values()

def get_message(id):
    return _messages[id]

def delete_message(msg):
    assert isinstance(msg, Message)
    del _messages[msg.id]

###

class User(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password

        self._save_user()

    def _save_user(self):
        self.id = _get_next_user_id()

        # register new user ID with the users list:
        _user_ids[self.id] = self
        _users[self.username] = self

def get_user(username):
    return _users.get(username) # return None if no such user

def get_all_users():
    return _users.values()

def delete_user(user):
    del _users[user.username]
    del _user_ids[user.id]
