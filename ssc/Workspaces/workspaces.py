# most standard and easy to understand libray
import psycopg2
from flask import jsonify, request


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