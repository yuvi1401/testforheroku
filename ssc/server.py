import os

from flask import Flask, jsonify, request, abort

from ssc.Invites.invites import getInvitesForUser, processInviteResponse

app = Flask(__name__, template_folder='testflask/templates')


@app.route("/")
def homeDummy():
    return 'Home';


@app.route("/api/invites/<username>", methods=["GET"])
def inviteUser(username):
    listOfInvites = getInvitesForUser(username)
    #TODO should return with a key called invites
    return jsonify(listOfInvites);

@app.route("/api/invites/<username>", methods=["POST"])
def updateInvite(username):
    print(username)
    print(request.json)
    if (not request.json) | ('accept' not in request.json) | ('workspace' not in request.json):
        abort(400)

    res = processInviteResponse(username, request.json)
    return jsonify({'invitesProcessed': res});


if __name__ == "__main__":
    # app.run(debug=True)
    port = int(os.environ.get('PORT', 5000))
    app.run( port=port)
