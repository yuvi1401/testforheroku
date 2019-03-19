# most standard and easy to understand libray
import psycopg2
from flask import jsonify, request
from cryptography.fernet import Fernet


def post_workspace_users(data):
    try:
        workspace_name = data['name']

        connection = psycopg2.connect(
            database='ssc'
        )

        cursor = connection.cursor()

        insert_workspace_name = "insert into workspaces (name) values (%s)"
        cursor.execute(insert_workspace_name, (workspace_name,))

        # workspace_list = cursor.fetchall()

        connection.commit()
        # select_all_workspaces = "select * from workspaces"
        # cursor.execute(select_all_workspaces)
        # all_workspaces = cursor.fetchall()

    except (Exception, psycopg2.Error) as error:
        print('Error while conecting to PostgresQL', error)
    finally:

        if (connection):
            # close the connection and the cursor
            cursor.close()
            connection.close()
            print("PostgresSQL connection is closed")

    return 'workspace added'


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

        select_workspace_id = "select workspace_id from workspaces where name = (%s)"
        cursor.execute(select_workspace_id, [workspace_name])
        workspace_id = cursor.fetchone()

        select_admin_boolean = "select is_admin from workspace_users where user_id = (%s) and workspace_id = (%s)"
        cursor.execute(select_admin_boolean, (user_id, workspace_id))
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


def encrypt_file(data):
    try:
        key = 'rfCFW5NYIJq5qWBLW_bXwHeg4z0PwVM9MDssLtQ-T4o='
        file_name = data['file_name']
        print(key)
        print(file_name)
        connection = psycopg2.connect(
            database='ssc'
        )
        cursor = connection.cursor()

        with open(file_name, 'rb') as f:
            file = f.read()

            # print(file)

            fernet = Fernet(key)
            encrypted = fernet.encrypt(file)
            print('!!!!!!!')
            print(encrypted)

        with open('file_to_encrypt', 'wb') as f:
            f.write(encrypted)
    except (Exception, psycopg2.Error) as error:
        print('Error while conecting to PostgresQL', error)

    finally:

        if (connection):
            # close the connection and the cursor
            cursor.close()
            connection.close()
            print("PostgresSQL connection is closed")

    return 'encrypted'
