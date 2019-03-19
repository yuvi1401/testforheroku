import psycopg2
from flask import jsonify

def fetch_users():


    try:
        connection = psycopg2.connect(
            user="willemtaylor",
            password="password",
            host="127.0.0.1",
            port="5432",
            database="ssc")
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM users;")
        user_records = cursor.fetchall()

        list_of_users = []
        for row in user_records:
            print("user_id = ", row[0])
            print("username = ", row[1])
            print("password = ", row[2], "\n")
            list_of_users.append({'username': row[1]})

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)

    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

    return jsonify({"users": list_of_users})
