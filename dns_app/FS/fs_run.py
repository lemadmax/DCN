from flask import Flask
from flask import request, abort, jsonify
import flask
from socket import *
app = Flask(__name__)

hostname = ''
ip = ''
as_ip = ''
as_port = 0
fs_socket = socket(AF_INET, SOCK_DGRAM)

@app.route('/')
def hello_world():
    return 'welcome to fabonacci server!'


@app.route('/register', methods=["PUT"])
def register():
    content = request.json
    hostname = content['hostname']
    ip = content['ip']
    as_ip = content['as_ip']
    as_port = content['as_port']
    message = 'TYPE=A\nNAME=fibonacci.com\nVALUE=' + ip + '\nTTL=10'
    fs_socket.sendto(message.encode(), (as_ip, as_port))
    response, serverAddr = fs_socket.recvfrom(2048)
    response_str = response.decode()
    if response_str == 'fail':
        return 'fail to register dns', 400
    
    return flask.Response(status=201)

@app.route('/fibonacci')
def fibonacci():
    number = request.args.get("number")
    n = int(number)
    if n is None:
        abort(400)
    if n == 1 or n == 2:
        return str(1), 200
    a = 1
    b = 1
    res = 0
    for i in range(2,n):
        res = a + b
        a = b
        b = res
    return str(res), 200

app.run(host='0.0.0.0',
        port=9090,
        debug=True)
