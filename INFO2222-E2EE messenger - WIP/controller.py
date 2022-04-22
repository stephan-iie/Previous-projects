'''
    This file will handle our typical Bottle requests and responses 
    You should not have anything beyond basic page loads, handling forms and 
    maybe some simple program logic
'''

from re import U
from bottle import route, get, post, error, request, static_file, response

import model


# -----------------------------------------------------------------------------
# Static file paths
# -----------------------------------------------------------------------------

# Allow image loading
@route('/img/<picture:path>')
def serve_pictures(picture):
    '''
        serve_pictures

        Serves images from static/img/

        :: picture :: A path to the requested picture

        Returns a static file object containing the requested picture
    '''
    return static_file(picture, root='static/img/')


# -----------------------------------------------------------------------------

# Allow CSS
@route('/css/<css:path>')
def serve_css(css):
    '''
        serve_css

        Serves css from static/css/

        :: css :: A path to the requested css

        Returns a static file object containing the requested css
    '''
    return static_file(css, root='static/css/')


# -----------------------------------------------------------------------------

# Allow javascript
@route('/js/<js:path>')
def serve_js(js):
    '''
        serve_js

        Serves js from static/js/

        :: js :: A path to the requested javascript

        Returns a static file object containing the requested javascript
    '''
    return static_file(js, root='static/js/')


# -----------------------------------------------------------------------------
# Pages
# -----------------------------------------------------------------------------

# Redirect to home page
@get('/')
@get('/home')
def get_home():
    '''
        get_index

        Serves the index page
    '''
    return model.home()


# -----------------------------------------------------------------------------

# Display the register page
@get('/register')
def get_register_controller():
    return model.register_form()


# -----------------------------------------------------------------------------

# Attempt the register 
@post('/register')
def post_register():
    username = request.forms.get('username')
    password = request.forms.get('password')
    response.set_cookie('potential_username', username)

    return model.register_check(username, password)


# -----------------------------------------------------------------------------

# Display the log out page
@get('/logout')
def get_logout_controller():
    return model.logout_form()


# -----------------------------------------------------------------------------

# Attempt the log out
@post('/logout')
def post_logout():
    # Call the appropriate method
    user = request.get_cookie("user")
    return model.logout_check(user)


# -----------------------------------------------------------------------------
# Display the chat page
@get('/chats')
def get_chats_controller():
    user=request.get_cookie("user")
    return model.chats_form(user)


# -----------------------------------------------------------------------------

# Display the login page
@get('/login')
def get_login_controller():
    '''
        get_login

        Serves the login page
    '''
    return model.login_form()


# -----------------------------------------------------------------------------

# Attempt the login
@post('/login')
def post_login():
    '''
        post_login

        Handles login attempts
        Expects a form containing 'username' and 'password' fields
    '''
    
    #todo Needs to check if the individual just visited valid register page, e.g. use a justRegistered cookie
    #todo if yes, need to store the pkey in db and change justRegistered cookie to no so we dont resave public key


    # Handle the form processing
    username = request.forms.get('username')
    password = request.forms.get('password')

    # Call the appropriate method
    return model.login_check(username, password)


# -----------------------------------------------------------------------------
# adding friends
@post("/addFriend")
def search_friends():
    friend = request.forms.get('friend')
    chatWith = request.forms.get('chatWith')
    pkey = request.cookies.get("PublicKey")
    user=request.get_cookie("user")

    # These were just here for debugging 
    print(pkey)
    print(request.cookies.keys())
    print(request.cookies.get("user"))
    print(request.cookies.get("currentChat"))
    print(request.cookies.get("currentChat"))

    if friend == None:
        return model.model_chatWith(chatWith,user)

    else:
        return model.model_add_friend(friend,user)


# -----------------------------------------------------------------------------

@get('/about')
def get_about():
    '''
        get_about
        
        Serves the about page
    '''
    return model.about()


# -----------------------------------------------------------------------------

# Help with debugging
@post('/debug/<cmd:path>')
def post_debug(cmd):
    return model.debug(cmd)


# -----------------------------------------------------------------------------

# 404 errors, use the same trick for other types of errors
@error(404)
def error(error):
    return model.handle_errors(error)


# -----------------------------------------------------------------------------

# Messaging

@post('/sendMessage')
def send_Message():
    chattingWith = request.get_cookie("currentChat" )
    user=request.get_cookie("user")
    return model.model_send_message(chattingWith, user)

@post('/displayMessage')
def display_Message():
    message = request.forms.get('CMsg')
    iv = request.forms.get('IV')
    msgTime = request.forms.get('msgTime')
    chattingWith = request.get_cookie("currentChat" )
    user=request.get_cookie("user")
    return model.model_process_message(message, chattingWith, user, msgTime, iv)

    
    

    