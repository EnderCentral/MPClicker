import json
import os

from flask import Flask, render_template, request, make_response

from game_database import Player

app = Flask(__name__, static_url_path='/static')


@app.route('/list/')
def log():
    return '<a href="/">back</a><br>' + '<br>'.join(map(str, Player.list()))


@app.route('/incr/', methods=['POST'])
def incr():
    player = Player.get_player('')
    player.clicks += request.get_json().get('clicks', 0)
    player.save()
    return json.dumps({
        'clicks': player.clicks
    })


@app.route('/')
def main():
    player = Player.get_player('')
    return render_template('cookie.html', player=player)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
