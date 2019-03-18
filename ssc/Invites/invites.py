import psycopg2

def getInvitesForUser(username):
    try:
        connection = psycopg2.connect(
            database="ssc")
        cursor = connection.cursor()

        getUserId_pgQuery = "select user_id from users where username=%s"

        cursor.execute(getUserId_pgQuery, (username,))
        userId = cursor.fetchone()

        if (userId == None):
            return []

        getInvites_pgQuery = "select * from invites where user_id=%s"
        cursor.execute(getInvites_pgQuery, (userId,))
        invitesForUser = cursor.fetchmany()

        #listOfInvites = []

        #for row in invitesForUser:



        #print (invitesForUser)

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        # closing database connection.
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

    return invitesForUser;


