import os
import random
import string

from flask import *

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'This is really unique and secret'


@app.route('/log/')
def log():
	return request.args.get('test')


@app.route('/test/')
def test():
	return redirect(
		url_for('log', test=''.join(random.choice(string.ascii_letters + string.digits) for i in range(64))))


@app.route('/')
def main():
	return render_template('Cockie.html')


if __name__ == '__main__':
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port, debug=True)