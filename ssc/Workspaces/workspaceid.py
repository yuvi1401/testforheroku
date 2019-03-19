import psycopg2


def fetch_workspace_id(workspace):
    try:
        connection = psycopg2.connect(
            database="ssc")
        cursor = connection.cursor()

        get_workspace_id_sql = "select workspace_id from workspaces where name=%s"

        cursor.execute(get_workspace_id_sql, (workspace,))
        workspace_id = cursor.fetchone()

        if (workspace_id is None):
            return -1

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

    return workspace_id
