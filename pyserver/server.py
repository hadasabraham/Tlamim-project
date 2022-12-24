from flask_socketio import SocketIO, emit
from flask import Flask
from flask_cors import CORS
from random import randint
from threading import Thread, Event
from time import sleep
import json

from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)
# Server functionality for receiving and storing data from elsewhere, not related to the websocket
#Data Generator Thread
thread = Thread()
thread_stop_event = Event()

# Handle the webapp connecting to the websocket
@socketio.on('connect')
def test_connect():
    print('someone connected to websocket')
    emit('responseMessage', {'data': [
    {
        "name": "Tmer",
        "email": "omer@gmail.com",
        "status": 2,
        "hide": "blabla"
    },]})
    # need visibility of the global thread object


# Handle the webapp connecting to the websocket, including namespace for testing
@socketio.on('connect', namespace='/devices')
def test_connect2():
    print('someone connected to websocket!')
    emit('responseMessage', {'data': 'Connected devices! ayy'})

# Handle the webapp sending a message to the websocket
@socketio.on('message')
def handle_message(message):
    with open("data"+str(randint(1,3))+".json", 'r') as f:
        data = f.read()
        data = json.loads(data)
    emit('responseMessage', {'data': data})
    
# Handle the webapp sending a message to the websocket
@socketio.on('search')
def handle_message(message):
    print("searching")
    with open("data3.json", 'r') as f:
        data = f.read()
        data = json.loads(data)
        print(data)
        out = [x for x in data if message['data'] in x['name']]
        print(out)
        data = out
        #data =  json.dumps(out)
        print(data)
    print([{
        "name": "Nadav",
        "email": "omer@gmail.com",
        "status": 2,
        "hide": "blabla1"
    }])
    emit('responseMessage', {'data': data })
    return
    with open("data"+str(randint(1,3))+".json", 'r') as f:
        data = f.read()
        data = json.loads(data)
        print(data)
        out = [x for x in data if message["data"] in x['name']]
        data = json.dumps(out)
    print(data)
    emit('responseMessage', {'data': [{'name': 'Nadav', 'email': 'omer@gmail.com', 'status': 2, 'hide': 'blabla1'}]})
    

# Handle the webapp sending a message to the websocket, including namespace for testing
@socketio.on('message', namespace='/devices')
def handle_message2():
    print('someone sent to the websocket!')


@socketio.on_error_default  # handles all namespaces without an explicit error handler
def default_error_handler(e):
    print('An error occured:')
    print(e)

if __name__ == '__main__':
    # socketio.run(app, debug=False, host='0.0.0.0')
    http_server = WSGIServer(('',5015), app, handler_class=WebSocketHandler)
    http_server.serve_forever()
