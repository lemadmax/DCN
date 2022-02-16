from datetime import datetime
from flask import Flask
from flask import request, abort
from socket import *
import requests
import flask
app = Flask(__name__)

fs_ip = "172.19.0.3"
fs_url = "http://172.19.0.2:9090/register/put"
fsn_url = "http://172.19.0.2:9090/fibonacci"

us_socket = socket(AF_INET, SOCK_DGRAM)

@app.route('/')
def hello_world():
    return 'welcome to user server!'

@app.route('/time')
def display_current_time():
    return str(datetime.now())

@app.route('/fibonacci')
def fibonacci():
    hostname = request.args.get("hostname")
    fs_port = request.args.get("fs_port")
    number = request.args.get("number")
    as_ip = request.args.get("as_ip")
    as_port = request.args.get("as_port")
    if hostname is None or fs_port is None or number is None or as_ip is None or as_port is None:
        abort(400)
    message = 'TYPE=A\nNAME=' + hostname
    us_socket.sendto(message.encode(), (as_ip, int(as_port)))
    response, serverAddr = us_socket.recvfrom(2048)
    response_str = response.decode()
    if response_str == 'fail':
        return 'unable to find the ip address of ' + hostname, 400
    fields = response_str.split()
    TYPE = fields[0].split('=')
    NAME = fields[1].split('=')
    VALUE = fields[2].split('=')
    TTL = fields[3].split('=')
    url = 'http://' + VALUE[1] + ':' + fs_port + '/fibonacci?number=' + number
    print(url)
    r = requests.get(url)
    print("fibonacci number: " + r.text)
    
    return 'fibonacci number of ' + number + ' is ' + r.text, 200


app.run(host='0.0.0.0',
        port=8080,
        debug=True)
