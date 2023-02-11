import os
import time

from flask import Flask, jsonify

from mcstatus import MinecraftServer

MC_SERVER = os.environ.get("MC_STATUS_SERVER", "127.0.0.1")

app = Flask(__name__, static_url_path="")


server = MinecraftServer.lookup(MC_SERVER)
last_ping = 0
cache = {}

def get_query():
    global last_ping
    global cache

    if time.time() - last_ping < 5:
        return cache

    query = server.query()
    status = server.status().raw

    # Trim extra data
    for key in ["forgeData", "favicon"]:
        if key in status:
            del status[key]

    cache = {
        "query": query.raw,
        "status": status,
        "players": query.players.names
    }

    last_ping = time.time()

    return cache

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/query')
def query():
    data = get_query()
    return jsonify(data)

@app.route('/players')
def players():
    data = get_query()
    numplayers = int(data["query"]["numplayers"])
    status = 404 if numplayers == 0 else 200

    return jsonify({"numplayers": numplayers}), status

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True, host="0.0.0.0", port=5000)
