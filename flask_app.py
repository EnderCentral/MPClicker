import os

from flask import Flask, render_template, request

from game_database import Player

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'This is really unique and secret'


@app.route('/list/')
def log():
    return '<a href="/">create player</a><br>'+'<br>'.join(map(str, Player.list()))


@app.route('/signin/', methods=['GET', 'POST'])
def sign_in():
    player = {}
    for key, value in dict(request.form).items():
        player[key] = value[0]
    Player.create_player(**player)
    return '<a href="/list/">all players</a><br>'+str(Player.get_player(request.form['username']))


@app.route('/')
def test():
    return '<a href="/list/">all players</a><br>'+"""
    <form action="/signin/" method="post">
    <fieldset>
    <legend>Sign in:</legend>
    Nickname:<br>
    <input type="text" name="username"><br>
    Password:<br>
    <input type="password" name="password">
    <input type="submit" value="Submit">
    </fieldset>
    </form>
"""


@app.route('/')
def main():
    return render_template('Cockie.html')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='localhost', port=port, debug=True)
