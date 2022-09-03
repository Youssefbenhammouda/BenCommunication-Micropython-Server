import ast
import hashlib
import json
import socket
import random
from ast import literal_eval
from Crypto.Cipher import AES
from hashlib import sha256
from typing import Callable

ENCODING = 'utf-8'
class server:
    GETID = b'/GETID'
    def __init__(self, localip, localport,keyfile = 'key.sec',timeout=10, bufferSize=4096) -> None:
        self.actions_handlers = {}
        self.timeout = timeout
        self.port = localport
        self.UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.UDPServerSocket.bind((localip, localport))
        self.bufferSize = bufferSize
        s = open(keyfile,"rb")
        self.key =  sha256(s.read()).digest()
        s.close()
    @staticmethod
    def generate_new_secret(file):
        rand = random.randbytes(32)
        with open(file,"wb") as f:
            f.write(rand)
            f.close()

    def encrypt(self,text):
        if type(text) == str:text = bytes(text,ENCODING)
        cipher = AES.new(self.key, AES.MODE_CBC)
        iv = cipher.iv
        padded = text + b" " * (16 - len(text) % 16)
        encrypted = cipher.encrypt(padded)
        return (encrypted,iv)
    def decrypt(self,encrypted, iv):
        cipher = AES.new(self.key, AES.MODE_CBC, iv=iv)
        decrypted = cipher.decrypt(encrypted).decode('utf-8').strip(" ")
        return decrypted
    def get_random_id(self):
        return bytes(str(random.randint(163732,99999999999)),ENCODING)
    def authentificate(self, id,payload,iv,hash):
        mk = id+payload+iv
        hash1 = hashlib.sha256(mk).digest()
        if hash == hash1:
            return True
        return False
    def _send_id(self):
        id = self.get_random_id()
        pair = self.encrypt(id)
        self.UDPServerSocket.sendto(pair[0], self.addr)
        self.UDPServerSocket.sendto(pair[1], self.addr)
        return id
    def _send(self,payload):
        self.UDPServerSocket.sendto(payload, self.addr) 
    def get_payload(self,data,id):
        data = ast.literal_eval(data.decode())
        
        payload = data['data']
        iv = data['iv']
        auth = self.authentificate(id, payload, iv, data['hash'])
        if not auth: raise Exception("Error intruder warning!")
        decrypted = self.decrypt(data['data'],data['iv'])
        try:
            decrypted = literal_eval(decrypted)
        except:
            raise Exception("Malformatted response!")
        return decrypted
                
    
    def send_payload(self, payload,id):
        if type(payload) in (str, bytes):pass
        elif type(payload) in (dict, list):payload = json.dumps(payload)
        else:
            raise Exception("Payload must be of type: str, bytes, dict or list")
        encrypted = self.encrypt(payload)
        self.UDPServerSocket.sendto(hashlib.sha256(id+encrypted[0]+encrypted[1]).digest(), self.addr)
        self.UDPServerSocket.sendto(encrypted[1], self.addr)
        self.UDPServerSocket.sendto(encrypted[0], self.addr)
    def add_action_handler(self,action: str, fun: Callable):
        self.actions_handlers |= {action:fun}
    def run(self,payload):
        try:
            action = payload["action"]
        except KeyError:
            raise KeyError("No action attribute was supplied.")
        try:
            fun = self.actions_handlers[action]
        except KeyError:
            raise KeyError(f"No function found to handle action '{action}'.")
        try:
            data = payload["data"]
        except KeyError:
            return {"data":fun()}
        return {"data":fun(data)}
    def start(self):
        while True:
            self.addr = None
            self.UDPServerSocket.settimeout(None)
            data,addr = self.UDPServerSocket.recvfrom(self.bufferSize)
            if data == self.GETID:
                self.addr = (addr[0],self.port)
                id = self._send_id()
                self.UDPServerSocket.settimeout(self.timeout)
                data,_ = self.UDPServerSocket.recvfrom(self.bufferSize)
                payload = self.get_payload(data,id)
                if "noreturn" in payload:
                    self.UDPServerSocket.sendto(b"ok",self.addr)
                    continue
                payload = self.run(payload)
                self.send_payload(payload,id)
        




