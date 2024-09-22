from flask import Flask
import os

app = Flask(__name__)

name = os.getenv('MYNAME', 'World')
port = os.getenv('PORT', '8000')

@app.route('/')
def hello_world():
    return f'Hello, {name}!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(port))