'''
    This is a file that configures how your server runs
    You may eventually wish to have your own explicit config file
    that this reads from.

    For now this should be sufficient.

    Keep it clean and keep it simple, you're going to have
    Up to 5 people running around breaking this constantly
    If it's all in one file, then things are going to be hard to fix

    If in doubt, `import this`
'''

# -----------------------------------------------------------------------------
import os
import sys
from bottle import run
import gunicorn
import hashlib

# -----------------------------------------------------------------------------
# You may eventually wish to put these in their own directories and then load 
# Each file separately

# For the template, we will keep them together

import model
import view
import controller

# -----------------------------------------------------------------------------

# It might be a good idea to move the following settings to a config file and then load them
# Change this to your IP address or 0.0.0.0 when actually hosting
host = 'localhost'

# Test port, change to the appropriate port to host
port = 8081

# Turn this off for production
debug = True


def run_server():
    '''
        run_server
        Runs a bottle server
    '''

    run( host=host, port=port, debug=debug, server='gunicorn', keyfile = 'localhost.key', certfile = 'localhost.crt') # https://bottlepy.org/docs/dev/tutorial.html 
# keyfile='info2222.key, certfile = 'info2222.cert')
#-----------------------------------------------------------------------------
# Optional SQL support
# Comment out the current manage_db function, and 
# uncomment the following one to load an SQLite3 database

import sql


def manage_db():
    '''
        manage_db
        Starts up and re-initialises an SQL databse for the server
    '''
    #database_args = ":memory:"  # Currently runs in RAM, might want to change this to a file if you use it
    sql_db = sql.SQLDatabase()
    salt = 'hfuskblafjpawfheukfg'.encode()
    admin_password = 'admin'.encode()
    digest_adminPwd = hashlib.pbkdf2_hmac('sha256', admin_password, salt, 10000).hex()
    sql_db.database_setup(digest_adminPwd)
    sql_db.table_message()
    sql_db.table_friendlist()
    sql_db.table_session()

# -----------------------------------------------------------------------------

# What commands can be run with this python file
# Add your own here as you see fit

command_list = {
    'manage_db': manage_db,
    'server': run_server
}

# The default command if none other is given
default_command = 'server'


def run_commands(args):
    '''
        run_commands
        Parses arguments as commands and runs them if they match the command list

        :: args :: Command line arguments passed to this function
    '''
    commands = args[1:]

    # Default command
    if len(commands) == 0:
        commands = [default_command]

    for command in commands:
        if command in command_list:
            command_list[command]()
        else:
            print("Command '{command}' not found".format(command=command))


# -----------------------------------------------------------------------------

run_commands(sys.argv)
