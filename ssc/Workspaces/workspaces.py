import psycopg2

from ssc.Utils.db_ops import get_workspace_id, get_user_id, is_user_admin


def delete_workspace(delete_request):
    deleted_by = delete_request['deleted_by']
    workspace = delete_request['workspace']
    workspace_id = get_workspace_id(workspace)
    deleted_by_id = get_user_id(deleted_by)
    if (workspace_id == -1 | deleted_by_id == -1):
        return False

    try:
        connection = psycopg2.connect(
            database="ssc")
        cursor = connection.cursor()

        admin_status = is_user_admin(deleted_by_id, workspace_id)

        if (admin_status == 0):
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


def update_admin(workspace, admin_request):
    username = admin_request['username']
    admin_username = admin_request['admin_username']
    make_admin = admin_request['make_admin']

    workspace_id = get_workspace_id(workspace)
    user_id = get_user_id(username)
    admin_id = get_user_id(admin_username)

    if (workspace_id == -1 | admin_id == -1 | user_id == -1):
        return False

    try:
        connection = psycopg2.connect(
            database="ssc")
        cursor = connection.cursor()

        admin_status = is_user_admin(admin_id, workspace_id)

        if (admin_status == 0):
            return False

        if (make_admin == 'True'):
            make_admin_bool = True;
        else:
            make_admin_bool = False;

        update_admin_sql = "update workspace_users set is_admin=%s where workspace_id=%s" \
                           "and user_id=%s"
        cursor.execute(update_admin_sql, (make_admin_bool, workspace_id, user_id))
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


def post_workspace_users(data):
    try:
        workspace_name = data['name']

        connection = psycopg2.connect(
            database='ssc'
        )
        print(workspace_name)

        cursor = connection.cursor()

        insert_workspace_name = "insert into workspaces (name) values (%s)"
        cursor.execute(insert_workspace_name, (workspace_name,))
        connection.commit()

    except (Exception, psycopg2.Error) as error:
        print('Error while conecting to PostgresQL', error)
    finally:

        if (connection):
            # close the connection and the cursor
            cursor.close()
            connection.close()
            print("PostgresSQL connection is closed")

    return 'workspace added'
