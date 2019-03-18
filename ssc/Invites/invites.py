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

        getInvites_pgQuery = """select w.name, u.username from invites i 
                            inner join workspaces w on i.workspace_id=w.workspace_id 
                            inner join users u on i.invited_by_id = u.user_id 
                            where i.user_id=%s"""
        cursor.execute(getInvites_pgQuery, (userId,))
        invitesForUser = cursor.fetchall()

        listOfInvites = []

        print(invitesForUser)
        for row in invitesForUser:
            listOfInvites.append({'workspace': row[0], 'invited_by': row[1]})

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        # closing database connection.
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

    return listOfInvites;


