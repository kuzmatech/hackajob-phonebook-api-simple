import os
from flask import Flask
from flask import jsonify
from flask import request
from flask import Response
from flask import make_response
from flask_restful import Api

app = Flask(__name__)
api = Api(app, prefix="/api")
secret = os.environ.get('SECRET_PASS')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)