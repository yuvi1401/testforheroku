import os

from flask import Flask, jsonify, request, abort

from ssc.Invites.invites import fetch_user_invites, process_invite, insert_user_invite

app = Flask(__name__, template_folder = 'testflask/templates')


@app.route("/")
def homeDummy():
    return 'Home';


@app.route("/api/invites/<username>", methods = ["GET"])
def get_user_invites(username):
    list_of_invites = fetch_user_invites(username)
    res = {'invites': list_of_invites}
    return jsonify(res);


@app.route("/api/invites/<username>", methods = ["POST"])
def update_invite(username):
    print(username)
    print(request.json)
    if (not request.json) | ('accept' not in request.json) | ('workspace' not in request.json):
        abort(400)

    res = process_invite(username, request.json)
    return jsonify({'invitesProcessed': res});


@app.route("/api/invites", methods = ["POST"])
def invite_user():
    print(request.json)
    if (not request.json) | ('username' not in request.json) \
            | ('workspace' not in request.json) | ('invitedBy' not in request.json):
        abort(400)

    res = insert_user_invite(request.json)
    res_json = {'user_invited': res}
    if (res == False): res_json['error'] = 'Could not invite user. Check user is admin or invite still exits'
    return jsonify(res_json);


@app.route('/api/users/<username>', method = ["GET"])
def fetch_user():


if __name__ == "__main__":
    # app.run(debug=True)
    port = int(os.environ.get('PORT', 5000))
    app.run(port = port)
