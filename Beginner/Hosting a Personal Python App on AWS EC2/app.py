from flask import Flask # type: ignore

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello from your EC2 Python App!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)