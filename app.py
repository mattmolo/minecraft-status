import os
import time

from flask import Flask, jsonify

from mcstatus import MinecraftServer

MC_SERVER = os.environ.get("MC_STATUS_SERVER", "127.0.0.1")

app = Flask(__name__, static_url_path="")


server = MinecraftServer.lookup(MC_SERVER)
last_ping = 0
cache = {}

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/query')
def players():
    global last_ping
    global cache

    if time.time() - last_ping < 5:
        return jsonify(cache)

    query = server.query()
    status = server.status()
    cache = {
        "query": query.raw,
        "status": status.raw
    }

    last_ping = time.time()

    return jsonify(cache)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True, host="0.0.0.0", port=5000)
