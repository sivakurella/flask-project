import datetime
from flask import Flask

app = Flask(__name__)

@app.route("/say-hello")
def hello():
    return 'Hello World!'

@app.route("/")
def tell_time():
    return 'Date and Time: ' + datetime.datetime.now().strftime("%Y-%m-%d, %H:%M:%S.%f")

if __name__ == '__main__':
    app.run()