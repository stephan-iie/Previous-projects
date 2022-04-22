import itertools
import sqlite3


# This class is a simple handler for all of our SQL database actions
# Practicing a good separation of concerns, we should only ever call 
# These functions from our models

# If you notice anything out of place here, consider it to your advantage and don't spoil the surprise

class SQLDatabase():
    '''
        Our SQL Database

    '''

    # Get the database running
    def __init__(self, database_arg="database.db"):
        self.conn = sqlite3.connect(database_arg)
        self.cur = self.conn.cursor()

    # SQLite 3 does not natively support multiple commands in a single statement
    # Using this handler restores this functionality
    # This only returns the output of the last command
    def execute(self, sql_string):
        out = None
        for string in sql_string.split(";"):
            try:
                out = self.cur.execute(string)
            except:
                pass
        return out

    # Return list from SQL
    def execute_list(self, sql_string):
        res = None
        for string in sql_string.split(";"):
            try:
                self.cur.execute(string)
                result = self.cur.fetchall()
                res = list(itertools.chain(*result))
            except:
                pass
        return res

    # Commit changes to the database
    def commit(self):
        self.conn.commit()

    # Return python dictionary from SQL
    def execute_dic(self, sql_string):
        data = None
        for string in sql_string.split(";"):
            try:
                self.cur.execute(string)
                desc = self.cur.description
                column_names = [col[0] for col in desc]
                data = [dict(zip(column_names, row))
                        for row in self.cur.fetchall()]
            except:
                pass
        return data

    # Return integer from SQL
    def execute_int(self, sql_string):
        result = None
        for string in sql_string.split(";"):
            try:
                self.cur.execute(string)
                res = self.cur.fetchone()
                result = int(res[0])
            except:
                pass
        return result

    # Return string from SQL
    def execute_str(self, sql_string):
        res = None
        for string in sql_string.split(";"):
            try:
                self.cur.execute(string)
                res = self.cur.fetchone()[0]
            except:
                pass
        return res

    # -----------------------------------------------------------------------------

    # Sets up the database
    # Default admin password
    def database_setup(self, admin_password):
        # Clear the database if needed
        self.execute("DROP TABLE IF EXISTS Users")
        self.commit()

        # Create the users table
        # status -> 0 means this user is not logged in. 1 means this user is logged in
        self.execute("""CREATE TABLE Users(
                    username VARCHAR(30) PRIMARY KEY,
                    password bit varying(5) NOT NULL,
                    status INTEGER DEFAULT 0,
                    admin INTEGER DEFAULT 0,
                    pkey TEXT,
                    spkey TEXT
                    )""")

        self.commit()

        # Add our admin user
        # self.add_user('admin', admin_password, status=0, admin=1,pkey="hiudbiubcd")

    # Create a table for storing messages
    def table_message(self):
        self.execute("DROP TABLE IF EXISTS Messages")
        self.commit()

        # Create the Messages table
        self.execute("""CREATE TABLE Messages(
                    sender VARCHAR(30) NOT NULL,
                    receiver VARCHAR(30) NOT NULL,
                    msg TEXT,
                    msgtime TEXT,
                    iv TEXT
                    )""")

        self.commit()

    # Create a table for storing friends
    def table_friendlist(self):
        self.execute("DROP TABLE IF EXISTS FriendList")
        self.commit()

        # Create the FriendList table
        self.execute("""CREATE TABLE FriendList(
                    username VARCHAR(30) NOT NULL,
                    friend VARCHAR(30) NOT NULL,
                    FOREIGN KEY (username) REFERENCES Users(username)
                    )""")

        self.commit()

    # Create a table for storing friends
    def table_session(self):
        self.execute("DROP TABLE IF EXISTS Session")
        self.commit()
        # Create the FriendList table
        self.execute("""CREATE TABLE Session(
                    conversation VARCHAR(30) NOT NULL,
                    ekey TEXT UNIQUE,
                    skey TEXT UNIQUE 
	   				)""")
        self.commit()

    # -----------------------------------------------------------------------------
    # User handling
    # -----------------------------------------------------------------------------

    # Add a user to the database
    def add_user(self, username, password, status, admin, pkey, spkey):
        sql_cmd = """
                INSERT INTO Users
                VALUES('{username}', '{password}', {status}, {admin}, '{pkey}', '{spkey}')
            """
        sql_cmd = sql_cmd.format(username=username.replace("'", "''"), password=password, status=status,
                                 admin=admin, pkey=pkey, spkey=spkey)

        self.execute(sql_cmd)
        self.commit()
        return True

    # -----------------------------------------------------------------------------
    # Update a user's status
    def update_user(self, username, status):
        sql_cmd = """
                UPDATE Users
                SET status = '{status}'
                WHERE username = '{username}'
                """
        sql_cmd = sql_cmd.format(username=username.replace("'", "''"), status=status)
        sql_cmd = sql_cmd.format()

        self.execute(sql_cmd)
        self.commit()
        return True

    # Add keys in to the table after user first log in
    def update_pkey(self, username, pkey):
        sql_cmd = """
                UPDATE Users
                SET pkey = '{pkey}'
                WHERE username = '{username}'
                """
        sql_cmd = sql_cmd.format(username=username.replace("'", "''"), pkey=pkey)
        sql_cmd = sql_cmd.format()

        self.execute(sql_cmd)
        self.commit()
        return True

    def update_spkey(self, username, spkey):
        sql_cmd = """
                UPDATE Users
                SET spkey = '{spkey}'
                WHERE username = '{username}'
                """
        sql_cmd = sql_cmd.format(username=username.replace("'", "''"), spkey=spkey)
        sql_cmd = sql_cmd.format()

        self.execute(sql_cmd)
        self.commit()
        return True

    # -----------------------------------------------------------------------------
    # Get a user's status
    def get_status(self, username):
        sql_cmd = """
                   SELECT status
                   FROM Users
                   WHERE username = '{username}'
                   """
        sql_cmd = sql_cmd.format(username=username.replace("'", "''"))
        sql_cmd = sql_cmd.format()
        status = self.execute_int(sql_cmd)
        self.commit()
        return status

    # -----------------------------------------------------------------------------
    # Check login credentials:
    # Check if the username exist
    def check_user(self, username):
        sql_query = """
                        SELECT 1
                        FROM Users
                        WHERE username = '{username}' 
                    """

        sql_query = sql_query.format(username=username.replace("'", "''"))
        self.execute(sql_query)
        self.commit()
        # If our query returns
        if self.cur.fetchone():
            return True
        else:
            return False

    # If the user exists, check if the password matches
    def check_password(self, username, password):
        sql_query = """
                        SELECT 1
                        FROM Users
                        WHERE username = '{username}' AND password = '{password}'
                    """

        sql_query = sql_query.format(username=username.replace("'", "''"), password=password)
        self.execute(sql_query)
        self.commit()
        # If our query returns
        if self.cur.fetchone():
            return True
        else:
            return False

    # -----------------------------------------------------------------------------
    # Adding friends and friend list management
    # -----------------------------------------------------------------------------
    # Add new friends
    def add_friends(self, username, friend):
        sql_query = """
                    INSERT INTO FriendList
                    VALUES('{username}', '{friend}')
                    """

        sql_query = sql_query.format(username=username.replace("'", "''"), friend=friend.replace("'", "''"))
        self.execute(sql_query)
        self.commit()

        return True

    # List all friends
    def list_friends(self, username):
        sql_query = """
                        SELECT friend
                        FROM FriendList
                        WHERE username = '{username}' 
                    """

        sql_query = sql_query.format(username=username.replace("'", "''"))
        friendlist = self.execute_list(sql_query)
        self.commit()
        return friendlist

    # -----------------------------------------------------------------------------
    # Message Management
    # -----------------------------------------------------------------------------

    # Store messages
    def add_msg(self, username, friend, msg, time, iv):
        sql_query = """
                       INSERT INTO Messages
                       VALUES('{username}', '{friend}', '{msg}', '{time}','{iv}')
                       """

        sql_query = sql_query.format(username=username.replace("'", "''"), friend=friend.replace("'", "''"),
                                     msg=msg.replace("'", "''"), time=time, iv=iv)
        self.execute(sql_query)
        self.commit()

        return True

    # List out all the msgs
    def list_msgs(self, username, friend):
        sql_query = """
                           SELECT sender, msg, msgtime, iv
                           FROM Messages
                           WHERE sender = '{username}' or sender = '{friend}'
                       """

        sql_query = sql_query.format(username=username.replace("'", "''"), friend=friend.replace("'", "''"))
        msgList = self.execute_dic(sql_query)
        self.commit()
        return msgList

    # -----------------------------------------------------------------------------
    # Delete msg from DB
    # -----------------------------------------------------------------------------
    def delete_msgs(self, u1, u2):
        sql_query = """
                       DELETE 
                       FROM Messages
                       WHERE (sender = '{u1}' and receiver = '{u2}') or (sender = '{u2}' and receiver = '{u1}')
                       """

        sql_query = sql_query.format(u1=u1, u2=u2)
        self.execute(sql_query)
        self.commit()

        return True
    # -----------------------------------------------------------------------------
    # Get public keys from DB
    # -----------------------------------------------------------------------------
    # Get the pk for encryption
    def get_pk(self, username):
        sql_cmd = """
                           SELECT pkey
                           FROM Users
                           WHERE username = '{username}'
                           """
        sql_cmd = sql_cmd.format(username=username.replace("'", "''"))
        sql_cmd = sql_cmd.format()
        pk = self.execute_str(sql_cmd)
        self.commit()
        return pk

    # Get the pk for signature
    def get_spk(self, username):
        sql_cmd = """
                           SELECT spkey
                           FROM Users
                           WHERE username = '{username}'
                           """
        sql_cmd = sql_cmd.format(username=username.replace("'", "''"))
        sql_cmd = sql_cmd.format()
        pk = self.execute_str(sql_cmd)
        self.commit()
        return pk

    # -----------------------------------------------------------------------------
    # Store session keys to DB
    # -----------------------------------------------------------------------------
    # Add the session into db
    def add_session(self, conversation, ekey, skey):
        sql_query = """
                       INSERT INTO Session
                       VALUES('{conversation}', '{ekey}', '{skey}')
                       """

        sql_query = sql_query.format(conversation=conversation, ekey=ekey, skey=skey)
        self.execute(sql_query)
        self.commit()

        return True

    # -----------------------------------------------------------------------------
    # Get session keys from DB
    # -----------------------------------------------------------------------------
    # Get the pk for encryption
    def get_ekey(self, c1, c2):
        sql_cmd = """
                           SELECT ekey
                           FROM Session
                           WHERE conversation = '{c1}' or conversation = '{c2}'
                           """
        sql_cmd = sql_cmd.format(c1=c1, c2=c2)
        sql_cmd = sql_cmd.format()
        ekey = self.execute_str(sql_cmd)
        self.commit()
        return ekey

    # Get the pk for signature
    def get_skey(self, c1, c2):
        sql_cmd = """
                    SELECT skey
                    FROM Session 
                    WHERE conversation = '{c1}' or conversation = '{c2}'
                  """
        sql_cmd = sql_cmd.format(c1=c1, c2=c2)
        sql_cmd = sql_cmd.format()
        skey = self.execute_str(sql_cmd)
        self.commit()
        return skey

    # -----------------------------------------------------------------------------
    # Delete session keys from DB
    # -----------------------------------------------------------------------------
    def delete_session(self, c1, c2):
        sql_query = """
                       DELETE 
                       FROM Session
                       WHERE conversation = '{c1}' or conversation = '{c2}'
                       """

        sql_query = sql_query.format(c1=c1, c2=c2)
        self.execute(sql_query)
        self.commit()

        return True



    # -----------------------------------------------------------------------------
    # Check if the conversation exist in the db
    # -----------------------------------------------------------------------------
    def check_conversation(self, c1, c2):
        sql_query = """
                        SELECT 1
                        FROM Session
                        WHERE conversation = '{c1}' or conversation = '{c2}'
                    """

        sql_query = sql_query.format(c1=c1, c2=c2)
        self.execute(sql_query)
        self.commit()
        # If our query returns
        if self.cur.fetchone():
            return True
        else:
            return False