import os

from flask import Flask, render_template

from ssc.users.users import fetch_users

app = Flask(__name__, template_folder='testflask/templates')


@app.route("/api/users")
def get_users():
    return fetch_users()


if __name__ == "__main__":
    # app.run(debug=True)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
