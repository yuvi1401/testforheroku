import psycopg2
import asyncio
from flask import jsonify
from ssc.dbconfig import user, password, database
from ssc.Invites.invites import get_user_id


def add_user(username, password):
    try:
        connection = psycopg2.connect(
            user=user,
            password=password,
            database=database)
        cursor = connection.cursor()

        cursor.execute("""INSERT INTO users (username, password)
                       VALUES (%s, %s) RETURNING *;"""
                       , (username, password))
        connection.commit()

    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

    return jsonify({"users": username})


def fetch_users():
    try:
        connection = psycopg2.connect(
            user=user,
            password=password,
            database=database)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM users;")
        user_records = cursor.fetchall()

        list_of_users = []
        for row in user_records:
            list_of_users.append({'username': row[1]})

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)

    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

    return jsonify({"users": list_of_users})


def fetch_user_workspaces(username):
    try:
        connection = psycopg2.connect(
            user=user,
            password=password,
            database=database)
        cursor = connection.cursor()

        loop = asyncio.new_event_loop()
        user_id = loop.run_until_complete(get_user_id(username))

        if user_id == -1:
            return []

        user_workspaces_sql = "SELECT w.name, wu.is_admin " \
                              "FROM workspaces w " \
                              "JOIN workspace_users wu ON wu.workspace_id = w.workspace_id " \
                              "WHERE wu.user_id =%s "

        cursor.execute(user_workspaces_sql, (user_id,))

        user_workspaces = cursor.fetchall()

        list_of_user_workspaces = []

        for row in user_workspaces:
            list_of_user_workspaces.append({'workspace': row[0],
                                            'is_admin': row[1]})

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
