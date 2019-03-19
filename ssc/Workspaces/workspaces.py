import psycopg2

from ssc.Utils.db_ops import get_workspace_id, get_user_id, is_user_admin

def delete_workspace(delete_request):
    deleted_by = delete_request['deleted_by']
    workspace = delete_request['workspace']
    workspace_id = get_workspace_id(workspace)
    deleted_by_id = get_user_id(deleted_by)
    if (workspace_id==-1 | deleted_by_id==-1):
        return False


    try:
        connection = psycopg2.connect(
            database="ssc")
        cursor = connection.cursor()

        admin_status = is_user_admin(deleted_by_id, workspace_id)

        if (admin_status==0):
            return False

        delete_workspace_sql = "delete from workspaces where workspace_id=%s"
        cursor.execute(delete_workspace_sql, (workspace_id,))
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

    if (count == 0): return False
    return True
