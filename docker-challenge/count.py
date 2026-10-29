import os
import socket
from flask import Flask
import redis

APP_NAME = os.environ.get("APP_NAME", "My App")
REDIS_HOST = os.environ.get("REDIS_HOST", "redis")
REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))

app = Flask(__name__)
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)

@app.route('/')
def welcome():
    return f'Welcome to {APP_NAME}'

@app.route('/count')
def count():
    visits = r.incr('visits')
    return f'{APP_NAME}: visit number {visits}, served by container {socket.gethostname()}'

@app.route('/health')
def health():
    try:
        r.ping()
        return {'status': 'ok', 'redis': 'up'}, 200
    except redis.exceptions.ConnectionError:
        return {'status': 'error', 'redis': 'down'}, 503

@app.route('/reset')
def reset():
    r.set('visits', 0)
    return 'Counter reset to 0'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)