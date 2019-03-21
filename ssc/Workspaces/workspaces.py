import asyncio

import psycopg2

from ssc.Utils.db_ops import get_workspace_id, get_user_id, is_user_admin
from ssc.dbconfig import user, password, database


def delete_workspace(delete_request):
    deleted_by = delete_request['deleted_by']
    workspace = delete_request['workspace']
    loop = asyncio.new_event_loop()
    workspace_id = loop.run_until_complete(get_workspace_id(workspace))

    loop = asyncio.new_event_loop()
    deleted_by_id = loop.run_until_complete(get_user_id(deleted_by))

    if (workspace_id == -1 | deleted_by_id == -1):
        return False

    try:
        connection = psycopg2.connect(
            user=user,
            password=password,
            database=database)
        cursor = connection.cursor()

        loop = asyncio.new_event_loop()
        admin_status = loop.run_until_complete(is_user_admin(deleted_by_id, workspace_id))

        if (admin_status == 0):
            return False

        delete_workspace_sql = "delete from workspaces where workspace_id=%s"
        cursor.execute(delete_workspace_sql, (workspace_id,))
        connection.commit()
        count = cursor.rowcount

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
        return False

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

    loop = asyncio.new_event_loop()
    workspace_id = loop.run_until_complete(get_workspace_id(workspace))

    loop = asyncio.new_event_loop()
    user_id = loop.run_until_complete(get_user_id(username))

    loop = asyncio.new_event_loop()
    admin_id = loop.run_until_complete(get_user_id(admin_username))

    if (workspace_id == -1 | admin_id == -1 | user_id == -1):
        return False

    try:
        connection = psycopg2.connect(
            user=user,
            password=password,
            database=database)
        cursor = connection.cursor()


        loop = asyncio.new_event_loop()
        admin_status = loop.run_until_complete(is_user_admin(admin_id, workspace_id))

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
        return False

    finally:
        # closing database connection.
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

    if (count == 0): return False
    return True


def create_workspace_only(data):
    try:
        workspace_name = data['name']
        admin = data['admin'];
        loop = asyncio.new_event_loop()
        admin_id = loop.run_until_complete(get_user_id(admin))


        connection = psycopg2.connect(
            user=user,
            password=password,
            database=database)

        insert_workspace_name = "insert into workspaces (name) values (%s) returning workspace_id"

        cursor = connection.cursor()
        cursor.execute(insert_workspace_name, (workspace_name,))

        connection.commit()
        count = cursor.rowcount
        if (count == 0):
            return False;

        new_workspace_id = cursor.fetchone()[0]

        add_user_to_workspace([admin_id], new_workspace_id, True)

    except (Exception, psycopg2.Error) as error:
        print('Error while connecting to PostgresQL', error)
        return False
    finally:

        if (connection):
            # close the connection and the cursor
            cursor.close()
            connection.close()
            print("PostgresSQL connection is closed")

    return True


def create_workspace_with_users(data):
    users = data['users'];
    admin = data['admin'];
    workspace = data['name'];

    try:
        connection = psycopg2.connect(
            database=database)

        cursor = connection.cursor()

        insert_workspace_sql = "insert into workspaces (name) values (%s) " \
                               "returning workspace_id"
        cursor.execute(insert_workspace_sql, (workspace,))
        connection.commit()

        count = cursor.rowcount
        if (count == 0):
            return count;

        new_workspace_id = cursor.fetchone()[0]
        loop = asyncio.new_event_loop()
        admin_id = loop.run_until_complete(get_user_id(admin))
        admin_added = add_user_to_workspace([admin_id], new_workspace_id, True);
        if (admin_added == 0):
            return admin_added;

        user_id_list = []
        for user in users:
            loop = asyncio.new_event_loop()
            single_user_id = loop.run_until_complete(get_user_id(user['username']))
            user_id_list.append(single_user_id)

        users_added = add_user_to_workspace(user_id_list, new_workspace_id);
    except (Exception, psycopg2.Error) as error:
        print('Error while conecting to PostgresQL', error)
        return 0
    finally:
        if (connection):
            # close the connection and the cursor
            cursor.close()
            connection.close()
            print("PostgresSQL connection is closed")

    return users_added;


def add_user_to_workspace(list_of_ids, workspace_id, is_admin=False):
    try:
        connection = psycopg2.connect(
            user=user,
            password=password,
            database=database)

        cursor = connection.cursor()
        insert_user_to_workspace_sql = "insert into workspace_users (user_id, workspace_id, is_admin) " \
                                       "values (%s,%s,%s) returning user_id"

        count = 0
        for user_id in list_of_ids:
            if (user_id != -1):
                cursor.execute(insert_user_to_workspace_sql, (user_id, workspace_id, is_admin))
                connection.commit()
                count += cursor.rowcount

    except (Exception, psycopg2.Error) as error:
        print('Error while connecting to PostgresQL', error)
        return 0
    finally:
        if (connection):
            # close the connection and the cursor
            cursor.close()
            connection.close()
            print("PostgresSQL connection is closed")

    return count


def delete_user_from_workspace(data):
    try:
        # check if admin_username is the same as the workspace_admins
        username = data['username']
        admin_username = data['admin_username']
        workspace_name = data['workspace_name']

        connection = psycopg2.connect(
            database='ssc'
        )

        cursor = connection.cursor()
        select_user = "select user_id from users where username = (%s)"
        cursor.execute(select_user, [username])
        user_id = cursor.fetchone()

        cursor.execute(select_user, [admin_username])
        admin_id = cursor.fetchone()

        select_workspace_id = "select workspace_id from workspaces where name = (%s)"
        cursor.execute(select_workspace_id, [workspace_name])
        workspace_id = cursor.fetchone()

        select_admin_boolean = "select is_admin from workspace_users where user_id = (%s) and workspace_id = (%s)"
        cursor.execute(select_admin_boolean, (admin_id, workspace_id))
        admin_boolean = cursor.fetchone()

        print(admin_boolean)

        if admin_boolean:
            delete_user = "delete from workspace_users where user_id =(%s) and workspace_id = (%s)"
            cursor.execute(delete_user, (user_id, workspace_id))
            connection.commit()

        elif (connection):
            cursor.close()
            connection.close()
            print("PostgresSQL connection is closed")
            return 'You are not the admin of this group or the user is not part of this group'

    except (Exception, psycopg2.Error) as error:
        print('Error while conecting to PostgresQL', error)

    finally:

        if (connection):
            # close the connection and the cursor
            cursor.close()
            connection.close()
            print("PostgresSQL connection is closed")

    return 'user deleted'


def fetch_workspace_files(name):
    try:
        connection = psycopg2.connect(
            database="ssc")

        print("Using Python variable in Pg Query")

        cursor = connection.cursor()
        if (name == None):
            return []

        loop = asyncio.new_event_loop()
        workspace_id = loop.run_until_complete(get_workspace_id(name))
        if (workspace_id == -1):
            return []


        cursor.execute("""SELECT file_name FROM workspace_files
               INNER JOIN workspaces ON workspaces.workspace_id = workspace_files.workspace_id
               WHERE workspaces.workspace_id = %s
               """, (workspace_id,))

        workspace_files = cursor.fetchall()

        list_of_files = []
        for row in workspace_files:
            list_of_files.append(
                {'file_name': row[0]})

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        # closing database connection.
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

    return list_of_files;
