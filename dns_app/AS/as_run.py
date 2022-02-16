from flask import Flask
from socket import *

as_port = 53533
as_socket = socket(AF_INET, SOCK_DGRAM)
as_socket.bind(('', as_port))

def handle_message(message, addr):
    print(message)
    fields = message.split()
    print(fields)
    TYPE = fields[0].split('=')
    NAME = fields[1].split('=')
    VALUE = None
    TTL = None
    if len(fields) > 2:
        VALUE = fields[2].split('=')
        TTL = fields[3].split('=')
    response = 'fail'
    if VALUE is not None:
        dns_record = open('dns_record.txt', mode = 'w+', encoding = 'utf-8')
        records = dns_record.readlines()
        records.append(TYPE[1] + ' ' + NAME[1] + ' ' + VALUE[1] + ' ' + TTL[1])
        dns_record.writelines(records)
        response = 'success'
        dns_record.close()
    else:
        dns_record = open('dns_record.txt', mode = 'r', encoding = 'utf-8')
        records = dns_record.readlines()
        print(records)
        for line in records:
            _fields = line.split()
            if _fields[1] == NAME[1]:
                response = 'TYPE=' + _fields[0] + '\nNAME=' + _fields[1] + '\nVALUE=' + _fields[2] + '\nTTL=' + _fields[3]
        dns_record.close()
    as_socket.sendto(response.encode(), addr)

def receive():
    while True:
        message, addr = as_socket.recvfrom(2048)
        handle_message(message.decode(), addr)

if __name__ == '__main__':
    receive()