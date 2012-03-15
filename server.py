'''
Copyright (c) 2012 Marcus McCurdy

Created 3/1/12
@author: Marcus McCurdy <marcus.mccurdy@gmail.com>
'''

from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
import namegen

app = Flask(__name__)

generator = namegen.Namegen()


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/generate')
def generate():
    count = request.args.get('count', default=1, type=int)
    if not 0 < count <= 1000:
        count = 1
    names = [generator.generate() for x in xrange(count)]
    return jsonify(names=names)


if __name__ == '__main__':
    app.run(debug=True)
