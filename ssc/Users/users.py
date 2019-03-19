import psycopg2
from ssc.dbconfig import user, password
from ssc.Invites.invites import get_user_id


def fetch_user_workspaces(username):
    try:
        connection = psycopg2.connect(
            user = user,
            password = password,
            database = "ssc")
        cursor = connection.cursor()

        user_id = get_user_id(username)

        if user_id == -1:
            return []

        user_workspaces_sql = "SELECT w.name " \
                              "FROM workspaces w " \
                              "JOIN workspace_users wu ON wu.workspace_id = w.workspace_id " \
                              "WHERE wu.user_id =%s "

        cursor.execute(user_workspaces_sql, (user_id,))

        user_workspaces = cursor.fetchall()

        list_of_user_workspaces = []

        for row in user_workspaces:
            list_of_user_workspaces.append({'workspace': row[0]})

        print(list_of_user_workspaces)



    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        # closing database connection.
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

    return list_of_user_workspaces
