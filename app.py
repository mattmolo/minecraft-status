import time
from flask import Flask, jsonify

from mcstatus import MinecraftServer

MC_SERVER = os.environ.get("MC_STATUS_SERVER", "127.0.0.1")

app = Flask(__name__, static_url_path="")
server = MinecraftServer.lookup(MC_SERVER)

last_ping = 0
players_cache = []

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/players')
def players():
    global last_ping
    global players_cache

    if time.time() - last_ping < 5:
        players = players_cache
    else:
        query = server.query()
        players = query.players.names
        players_cache = players
        last_ping = time.time()


    return jsonify({
        'players': players
    })

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True, host="0.0.0.0", port=4000)
