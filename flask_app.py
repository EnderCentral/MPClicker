import os

from flask import Flask, render_template, request, make_response

from game_database import Player

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'This is really unique and secret'


@app.route('/list/')
def log():
    return '<a href="/">create player</a><br>' + '<br>'.join(map(str, Player.list()))


@app.route('/signin/', methods=['POST'])
def sign_in():
    player = Player.get_player(request.form['username'])
    if player is None:
        player = {}
        for key, value in dict(request.form).items():
            player[key] = value[0]
        player = Player.create_player(**player)
    response = make_response('<a href="/list/">all players</a><br>' + str(player))
    response.set_cookie('username', player.username)
    response.set_cookie('password', player.password)
    return response


@app.route('/login/')
@app.route('/register/')
def register():
    return '<a href="/list/">all players</a><br>'"""
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
    return '<a href="/list/">all players</a><br>' \
           '<a href="/login/">login</a><br>' \
           """<script>
           incr_xhr = new XMLHttpRequest();
           incr_xhr.onload = function (){
               document.getElementById("clicks").innerHTML = incr_xhr.response
           }
           handle_click = function(){
               incr_xhr.open("POST", '/incr/');
               incr_xhr.send(1)
           }
           </script>""" \
           '<button type="button" onclick="handle_click()">Click Me!</button>' \
           '<p id="clicks"></p>'
    return render_template('Cockie.html')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
