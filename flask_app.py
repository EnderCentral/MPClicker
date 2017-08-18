import os

from flask import Flask, render_template, request, make_response

from game_database import Player

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'This is really unique and secret'


@app.route('/list/')
def log():
    return '<a href="/">back</a><br>' + '<br>'.join(map(str, Player.list()))


@app.route('/signin/', methods=['POST'])
def sign_in():
    player = Player.get_player(request.form['username'])
    if player is None:
        player = {}
        for key, value in dict(request.form).items():
            player[key] = value[0]
        player = Player.create_player(**player)
    response = make_response('<a href="/">back</a><br>' + str(player))
    response.set_cookie('username', player.username)
    response.set_cookie('password', player.password)
    return response


@app.route('/login/')
@app.route('/register/')
def register():
    return render_template('register.html')


@app.route('/incr/', methods=['POST'])
def incr():
    player = None
    if 'username' in request.cookies and 'password' in request.cookies:
        player = Player.get_player_if_auth(request.cookies['username'], request.cookies['password'])
        if player:
            if request.data.decode():
                player.clicks += 1
                player.save()
    return str(player.clicks) if player else request.data.decode()


@app.route('/')
def main():
    if 'username' in request.cookies and 'password' in request.cookies:
        player = Player.get_player_if_auth(request.cookies['username'], request.cookies['password'])
        if player:
            return render_template('cookie.html', player=player)
    return render_template('cookie.html')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
