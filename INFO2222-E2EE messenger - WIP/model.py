'''
    Our Model class
    This should control the actual "logic" of your website
    And nicely abstracts away the program logic from your page loading
    It should exist as a separate layer to any database or data structure that you might be using
    Nothing here should be stateful, if it's stateful let the database handle it
'''
from email import message
import hashlib
from operator import itemgetter

import sql
import view
import random
from bottle import response, request
import datetime

# Initialise our views, all arguments are defaults for the template
page_view = view.View()

# Db instance
db = sql.SQLDatabase()



# -----------------------------------------------------------------------------
# Home
# -----------------------------------------------------------------------------

def home():
    '''
            index
            Returns the view for home
        '''
    return page_view("home")


# -----------------------------------------------------------------------------
# Register
# -----------------------------------------------------------------------------

def register_form():
    '''
        login_form
        Returns the view for the login_form
    '''
    return page_view("register")


def register_check(username, password):
    if username is None or password is None or username == "" or password == "":
        err_str = "Please enter something :("
        return page_view("invalidRegister", reason=err_str)

    # Check if user already exists in the database
    if db.check_user(username):
        err_str = "Oh no! This username has been taken. Please create another one :)"
        return page_view("invalidRegister", reason=err_str)
    else:
        # Hash + salt the password
        salt = 'hfuskblafjpawfheukfg'.encode()
        users_password = password.encode()
        password = hashlib.pbkdf2_hmac('sha256', users_password, salt, 10000).hex()
        # Add user's info into db
        db.add_user(username, password, 0, 0, "A", "A")

        return page_view("validRegister", reason="You are signed up! Welcome to the server!")


# -----------------------------------------------------------------------------
# Login
# -----------------------------------------------------------------------------

def login_form():
    '''
        login_form
        Returns the view for the login_form
    '''
    return page_view("login", reason="")


# Check the login credentials
    #TO DO: Extract the PublicKeyEd and PublicKeySv secret key and store both (Ed is for encryption, Sv is for signing) if they just registered 

def login_check(username, password):
    '''
        login_check
        Checks usernames and passwords

        :: username :: The username
        :: password :: The password

        Returns either a view for valid credentials, or a view for invalid credentials
    '''
    salt = 'hfuskblafjpawfheukfg'.encode()
    users_password = password.encode()
    password = hashlib.pbkdf2_hmac('sha256', users_password, salt, 10000).hex()
    # User not exist
    if not db.check_user(username):
        err_str = "You have not signed up yet! Please sign up first :)"
        return page_view("login", reason=err_str)
    # Wrong password
    elif not db.check_password(username, password):
        err_str = "Wrong Password :( Please enter again"
        return page_view("login", reason=err_str)
    else:
        # Get the public key for encryption from cookie
        pkey = request.cookies.get("PublicKeyEd")
        # Get the public key for signature from cookie
        spkey = request.cookies.get("PublicKeySv")

        print("=== inside login, setting pkey and seky ===")
        print(pkey)
        print(spkey)
        print("===")

        # Store the public key in to db
        if db.get_spk(username) == "A" and db.get_pk(username) == "A":
            db.update_pkey(username, pkey)
            db.update_spkey(username, spkey)
        # Successfully logged in, show user's friend list
        friends = db.list_friends(username)
        # Mark the user
        response.set_cookie("user", username)  
        response.set_cookie("currentChat", "Server")  # MEANS WE AR CURRENTLY ONLY TALKING TO SERVER
        msgTime = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        # Check if this user has logged in elsewhere already
        status = db.get_status(username)
        if status == 1:
            messages = [{"sender": "Server",
                         "msg": "[Warning!] You are already logged in elsewhere. If it's not you, please change your password immediately.",
                         "msgtime": msgTime},
                        {"sender": "Server", "msg": "What are you waiting for? Start chatting now XD", "msgtime": msgTime}]
            return page_view("friends", outcome="", data=friends, friend="Server",
                             messages=messages)
        else:
            # Update user's status
            db.update_user(username, 1)
            messages = [ {"sender": "Server", "msg": "What are you waiting for? Start chatting now XD", "msgtime": msgTime}]
            return page_view("friends", outcome="", data=friends, friend="Server",
                             messages=messages)

# -----------------------------------------------------------------------------
# Log Out
# -----------------------------------------------------------------------------

def logout_form():

    return page_view("logout", reason="")

def logout_check(USER):
    # Sign out this user in DB
    db.update_user(USER, 0)
    # Get the friend list of the user
    friend_list = db.list_friends(USER)
    # Loop through the friend list see if any friend has also logged out
    for f in friend_list:
        if db.get_status(f) == 0:
            # Get two possible combination of the conversation code
            c1 = f + USER
            c2 = USER + USER
            # Delete sesion
            db.delete_session(c1, c2)
            # Delete message
            db.delete_msgs(USER, f)

    # Check if both users in a conversation have logged out
    response.set_cookie("user", "")
    response.delete_cookie("secretSigned" )
    response.delete_cookie("secretEncrypted" )
    response.delete_cookie("friendKeyEd" )
    response.delete_cookie("friendKeySv" )
    response.delete_cookie("secret" )
    response.delete_cookie("secretExtracted" )
    return page_view("home", reason="")

# -----------------------------------------------------------------------------
# back to chats
# -----------------------------------------------------------------------------
def chats_form(USER):
    msgTime = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    friends = db.list_friends(USER)
    messages = [{"sender": "Server", "msg": "What are you waiting for? Start chatting now XD", "msgtime": msgTime}]
    return page_view("friends", outcome="", data=friends, friend="Server",
                     messages=messages)

# -----------------------------------------------------------------------------
# add friend 
# -----------------------------------------------------------------------------

 # TO DO: add the newly added friends public key (PublicKeySv) and (PublicKeyEd)
# as two new cookies so we can extract it when we click message (assumed only chat with this friend though)

def model_add_friend(friend, USER):
    msgTime = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    friends = db.list_friends(USER)
    messages = [{"sender": "Server", "msg": "What are you waiting for? Start chatting now XD", "msgtime": msgTime}]

    if db.check_user(friend):
        # If the user has already added this person as friend
        if friend in friends:
            # Add the friends pkey and spkey as a cookie so we can verify things 
            print("============Inside add friend (already added)================")
            print("friend {} pk: {}".format(friend,db.get_pk(friend)))
            print( "friend {} spk: {}".format(friend, db.get_spk(friend)))
            print("=============================================================")            
            response.set_cookie("friendKeyEd", db.get_pk(friend))
            response.set_cookie("friendKeySv", db.get_spk(friend))

            return page_view("friends", outcome="You guys are already friends XD", data=friends, friend="Server",
                             messages=messages)
        # If the user is trying to add him/herself as friend
        elif USER == friend:
            return page_view("friends", outcome="You can't add yourself as friend :(", data=friends, friend="Server",
                             messages=messages)
        else:
            db.add_friends(USER, friend)
            db.add_friends(friend, USER)
            friends = db.list_friends(USER)
            # Add the friends pkey and spkey as a cookie so we can verify things 
            print("===================Inside add friend ========================")
            print("friend {} pk: {}".format(friend,db.get_pk(friend)))
            print( "friend {} spk: {}".format(friend, db.get_spk(friend)))
            print("=============================================================")            
            response.set_cookie("friendKeyEd", db.get_pk(friend))
            response.set_cookie("friendKeySv", db.get_spk(friend))
            return page_view("friends", outcome="Success! Friend added :)", data=friends, friend="Server",
                             messages=messages)
    else:
        return page_view("friends", outcome="Cannot find username :( Please try again.", data=friends, friend="Server",
                         messages=messages)


# -----------------------------------------------------------------------------
# Chat with friend 
# -----------------------------------------------------------------------------


def model_chatWith(chatWith, USER):
    friends = db.list_friends(USER)
    if db.check_user(chatWith):  # check we can exist
        # todo Extract the signed and encrypted shared secret and save it in a schema with key being user and friend chatting wiht (change as see fit).
        # secretEncrypted , secretSigned is what youre looking for
        # IF entry alreay exists in the schema, it means the friend alreay shared a secret, save if for the other friend if this is the case
        # OLD NOTES---------------------------------------
        # Create a cookie which extracts the public key of the friend theyre currnetly chatting with talking to and
        # stores it for encryption purposes
        # This cookie will be extracted on clients end with JS
        # response.set_cookie("user", "")
        skey = request.cookies.get("secretSigned")
        ekey = request.cookies.get("secretEncrypted")
        extracted = request.cookies.get("secretExtracted")
        # todo the secret keys can not be sent to the server the first time the user clicked message button now
        #  the program will ignore the first attempt (Will fix it later)
        # Get two possible combination of the conversation code
        c1 = chatWith + USER
        c2 = USER + chatWith

        #If there is an entry in the table AND we havent exytacyed the cookie before , return the secrets as a cookie 
        if extracted ==None and db.check_conversation(c1, c2):
            ek=db.get_ekey(c1, c2)
            sk=db.get_skey(c1, c2)
            friends = db.list_friends(USER)
            print("=================storing as cookie from db =================")
            print(ek)
            print(sk)
            print("=============================================================") 
            response.set_cookie("secretSigned",sk )
            response.set_cookie("secretEncrypted",ek )
            response.set_cookie("secretExtracted","False" )


        # Store the secrets into the session table IF there is no entry previously 
        if skey is not None and ekey is not None: 
            # Check if the conversation exist in the db already
            if not db.check_conversation(c1, c2):
                db.add_session(c1, ekey, skey)
                # Just for testing
                print("=====================storing in db ==========================")
                print(db.get_ekey(c1, c2))
                print(db.get_skey(c1, c2))
                print("=============================================================")
                response.set_cookie("secretExtracted", "True")

        # Else we have no keys AND no entries 
        else:
            print("nokey")
        # To store the conversations
        response.set_cookie("currentChat", chatWith)
        messages = ex_con(chatWith,USER)

        return page_view("friends", outcome="", data=friends, friend=chatWith, messages=messages)

# -----------------------------------------------------------------------------
# Send message to friend
# ----------------------------------------------------------------------------- !!!!!!!!!!still implementing !!!!!!!!!

def model_process_message(message, chattingWith, USER, msgTime, iv):
    friends = db.list_friends(USER)
    #msgTime = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print("inside model_send_message: {}".format(chattingWith))
    if chattingWith is not None and db.check_user(chattingWith) and message is not None:
        # Store msg into Messages table
        db.add_msg(USER, chattingWith, message, msgTime, iv)
        messages = ex_con(chattingWith,USER)
        print("================= Encrypted Msg Test!!!!!!! =================")
        print(messages)
        print("=============================================================") 
        return page_view("friends", outcome="", data=friends, friend=chattingWith, messages=messages)

def model_send_message(chattingWith,USER):
    friends = db.list_friends(USER)
    messages = ex_con(chattingWith,USER)
    return page_view("friends", outcome="", data=friends, friend=chattingWith, messages=messages)
# -----------------------------------------------------------------------------
# Extract conversations from DB
# -----------------------------------------------------------------------------
def ex_con(chattingWith,USER):
    myMsg = db.list_msgs(USER, chattingWith)
    # Keep it in case it's useful later
    '''
    friendMsg = db.list_msgs(chattingWith, USER)
    messages = []
    myMsg.extend(friendMsg)
    for msgDic in myMsg:
        if msgDic not in messages:
            messages.append(msgDic)
    '''
    # Sort the conversation by time
    # sorted_messages = sorted(messages, key=itemgetter('msgtime'))
    return myMsg



# -----------------------------------------------------------------------------
# About
# -----------------------------------------------------------------------------

def about():
    '''
        about
        Returns the view for the about page
    '''
    return page_view("about", garble=about_garble())


# Returns a random string each time
def about_garble():
    '''
        about_garble
        Returns one of several strings for the about page
    '''
    garble = ["leverage agile frameworks to provide a robust synopsis for high level overviews.",
              "iterate approaches to corporate strategy and foster collaborative thinking to further the overall value proposition.",
              "organically grow the holistic world view of disruptive innovation via workplace change management and empowerment.",
              "bring to the table win-win survival strategies to ensure proactive and progressive competitive domination.",
              "ensure the end of the day advancement, a new normal that has evolved from epistemic management approaches and is on the runway towards a streamlined cloud solution.",
              "provide user generated content in real-time will have multiple touchpoints for offshoring."]
    return garble[random.randint(0, len(garble) - 1)]


# -----------------------------------------------------------------------------
# Debug
# -----------------------------------------------------------------------------

def debug(cmd):
    try:
        return str(eval(cmd))
    except:
        pass


# -----------------------------------------------------------------------------
# 404
# Custom 404 error page
# -----------------------------------------------------------------------------

def handle_errors(error):
    error_type = error.status_line
    error_msg = error.body
    return page_view("error", error_type=error_type, error_msg=error_msg)
