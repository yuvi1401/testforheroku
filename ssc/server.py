import os

from flask import Flask, request

from ssc.Workspaces.workspaces import *

app = Flask(__name__, template_folder='testflask/templates')


@app.route("/")
def homeDummy():
    return 'Home';


@app.route("/users")
def usersDummy():
    return "Hello, Users"

@app.route("/deleteUser", methods=['DELETE'])
def delete_user():
    return delete_user_from_workspace(request.json)


@app.route('/api/workspaces', methods=['POST'])
def Workspaces_users():

    return post_workspace_users(request.json)


if __name__ == "__main__":
    # app.run(debug=True)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)