import psycopg2
from flask import jsonify


def fetch_user_details(username, password):


    try:
        connection = psycopg2.connect(
            user="willemtaylor",
            password="password",
            host="127.0.0.1",
            port="5432",
            database="ssc")
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s;", (username, password))
        count = cursor.rowcount

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)

    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
    if count == 0:
        return jsonify({"user_exists": False})
    else:
        return jsonify({"user_exists": True})
