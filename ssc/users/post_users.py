import psycopg2
from flask import jsonify, request


def add_user(username, password):


    try:
        connection = psycopg2.connect(
            user="willemtaylor",
            password="password",
            host="127.0.0.1",
            port="5432",
            database="ssc")
        cursor = connection.cursor()

        cursor.execute("""INSERT INTO users (username, password)
                       VALUES (%s, %s) RETURNING *;"""
                       , (username, password))
        connection.commit()

        # except (Exception, psycopg2.Error) as error:
        # print("Error while connecting to PostgreSQL", error)

    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

    return jsonify({"users": username})
