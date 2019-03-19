import os

from flask import Flask, render_template, request

from ssc.users.get_users import fetch_users
from ssc.users.post_users import add_user

app = Flask(__name__, template_folder='testflask/templates')


@app.route("/api/users")
def get_users():
    return fetch_users()

@app.route("/api/users", methods=['POST'])
def post_user():
    username = request.json['username']
    password = request.json['password']
    return add_user(username, password)


if __name__ == "__main__":
    # app.run(debug=True)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
