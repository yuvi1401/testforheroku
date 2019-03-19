import os

from flask import Flask, jsonify, request, abort

from ssc.Workspaces.workspace import fetch_workspace_files
from ssc.Workspaces.workspaceid import fetch_workspace_id

app = Flask(__name__, template_folder='testflask/templates')


@app.route("/")
def homeDummy():
    return 'Home';


@app.route("/api/workspaces/<name>", methods=["GET"])
def get_workspace_file(name):
    list_of_files = fetch_workspace_files(name)
    res = {'files': list_of_files}
    return jsonify(res);

if __name__ == "__main__":
    # app.run(debug=True)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
