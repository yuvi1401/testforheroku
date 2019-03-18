import os
#import json

from flask import Flask, jsonify

from ssc.Invites.invites import getInvitesForUser

app = Flask(__name__, template_folder='testflask/templates')


@app.route("/")
def homeDummy():
    return 'Home';


@app.route("/api/invites/<username>", methods=["GET"])
def inviteUser(username):
    listOfInvites = getInvitesForUser(username)
    print (listOfInvites)
    res = {'workspaces': listOfInvites}

    #inviteCount = len(listOfInvites)
    #if (inviteCount>0):
        #res['invites'] = len(listOfInvites)

    return jsonify(res);

@app.route("/users")
def usersDummy():
    return "Hello, Users"


if __name__ == "__main__":
    # app.run(debug=True)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
