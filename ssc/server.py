import os

from flask import Flask, jsonify

from ssc.Invites.invites import getInvitesForUser

app = Flask(__name__, template_folder='testflask/templates')


@app.route("/")
def homeDummy():
    return 'Home';


@app.route("/api/invites/<username>", methods=["GET"])
def inviteUser(username):
    listOfInvites = getInvitesForUser(username)
    return jsonify(listOfInvites);

@app.route("/users")
def usersDummy():
    return "Hello, Users"


if __name__ == "__main__":
    # app.run(debug=True)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
