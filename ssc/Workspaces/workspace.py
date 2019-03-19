import psycopg2

from ssc.Workspaces.workspaceid import fetch_workspace_id


def fetch_workspace_files(name):
    try:
        connection = psycopg2.connect(
            database="ssc")

        print("Using Python variable in Pg Query")

        cursor = connection.cursor()
        if (name == None):
            return []
        workspaceid = fetch_workspace_id(name)
        print(workspaceid)
        cursor.execute("""SELECT file_name FROM workspace_files
               INNER JOIN workspaces ON workspaces.workspace_id = workspace_files.workspace_id
               WHERE workspaces.workspace_id = %s
               """, (workspaceid,))


        # cursor.execute("SELECT workspace_id, name FROM workspaces WHERE workspaces.name = %s", (name,))

        workspace_files = cursor.fetchall()

        list_of_files = []
        for row in workspace_files:
            list_of_files.append(
                {'file_name': row[0]})
        # list_of_files = []
        #
        # for row in workspace_files:
        #     list_of_files.append({'workspaceId': row[0], 'workspaceName': row[1]})

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        # closing database connection.
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

    return list_of_files;
