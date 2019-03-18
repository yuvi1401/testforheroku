import psycopg2

#TODO reuse methods everywhere

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


def processInviteResponse(username, inviteResponse):
    decision = inviteResponse['accept']
    workspace = inviteResponse['workspace']

    try:
        connection = psycopg2.connect(
            database="ssc")
        cursor = connection.cursor()

        getInviteId_pgQuery = """select i.invite_id, i.user_id, i.invited_by_id, i.workspace_id
                                    from invites i, users u, workspaces w 
                                    where u.username=%s and w.name=%s
                                    and u.user_id=i.user_id and w.workspace_id=i.workspace_id"""

        cursor.execute(getInviteId_pgQuery, (username,workspace))
        invites = cursor.fetchone()
        if (invites == None):
            return []

        inviteId=invites[0]
        userId=invites[1]
        invitedBy = invites[2]
        workspaceId = invites[3]


        print(inviteId, userId, workspaceId, invitedBy)

        if (decision == True):
            print('true')
            insertUserWorkspace_pgQuery = """insert into workspace_users (user_id, workspace_id, is_admin)
                                        values(%s, %s, false)"""
            cursor.execute(insertUserWorkspace_pgQuery, (userId, workspaceId))
            connection.commit()
            count = cursor.rowcount

            if (count==0):
                return 0;

            deleteInvite_pgQuery = "delete from invites where invite_id=%s"
            cursor.execute(deleteInvite_pgQuery, (inviteId,))
            connection.commit()
            count = cursor.rowcount

        else:
            print('false')
            deleteInvite_pgQuery = "delete from invites where invite_id=%s"
            cursor.execute(deleteInvite_pgQuery, (inviteId,))
            connection.commit()
            count = cursor.rowcount


    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        # closing database connection.
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

    return count