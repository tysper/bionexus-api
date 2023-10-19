from flask import Flask, request
from flask_restful import Api, Resource
from datetime import datetime
import uuid
import json

app = Flask(__name__)
api = Api(app)

class Log:
    def __init__(self, log_name):
        self.log_name = log_name

        open(f"{log_name}", "+a").close()

    def start(self):
        try:
            self.file = open(f"{self.log_name}", "+a")
            return True
        except:
            print(f"[Error]: '{self.log_name}' could not be opened.")
            return False
        
    def write(self, message, type):
        now = datetime.now()

        try:
            self.file.write(f"\n{now} [{type}]: {message}")
            return True
        except:
            print(f"[Error]: '{self.log_name}' must be opened before writing to it.")
            return False
        
    def end(self):
        try:
            self.file.close()
            return True
        except:
            print(f"[Error]: '{self.log_name}' could not be closed.")
            return False

    def clear(self):
        try:
            open(f"{self.log_name}", "w").close()
            return True
        except:
            print(f"[Error]: '{self.log_name}' was not cleared.")
            return False

    def __str__(self):
        try:
            result = ""
            file = open(f"{self.log_name}", "r")
            for line in file.readlines():
                result+=line
            file.close()
            return result
        except:
            print(f"[Error]: '{self.log_name}' could not be red.")
            return ""

server_log = Log("./logs/server_log.txt")
server_log.start()
server_log.end()




class Connection:
    def __init__(self, connection_uuid, esp32, device):
        self.connection_uuid = connection_uuid
        self.esp32 = esp32
        self.device = device

    def __str__(self):
        return f"Connection UUID: {self.connection_uuid}\n\tESP32:\n\t\tIP Address:{None if not self.esp32 else self.esp32.ip_address}\n\t\tConnection Instance: {None if not self.esp32 else self.esp32.connection_instance}\n\tCellphone:\n\t\tIP Address:{None if not self.device else self.device.ip_address}\n\t\tConnection Instance: {None if not self.device else self.device.connection_instance}"

class Device:
    def __init__(self, ip_address, connection_instance):
        self.ip_address = ip_address
        self.connection_instance = connection_instance




class Esp32(Device):
    pass

    
        
class Cellphone(Device):
    pass


# connections = [(Connection("cbdceeb3-d9f0-4987-8e8c-95b4ec91523f", esp32=Esp32("192.168.0.1", {}), device=Cellphone("192.168.0.1", {})))]
connections = []














#command → device=cellphone&uuid=cbdceeb3-d9f0-4987-8e8c-95b4ec91523f
#command → device=esp&uuid=cbdceeb3-d9f0-4987-8e8c-95b4ec91523f

class StartConnection(Resource):
    def get(self):
        command = request.form.to_dict(flat=True)
        ip_address = request.remote_addr

        server_log.start()
        
        device = command["device"]
        device_uuid = command["uuid"]

        connection_exists = False
        current_connection = None

        for connection in connections:
            if(connection.connection_uuid == device_uuid):
                connection_exists = True
                current_connection = connection
                break
        
        if(connection_exists):
            server_log.write(f"A connection with UUID: {device_uuid} already exists connecting to existing connection.", "info")
            server_log.write(f"Device type: {device}.", "info")
            if(device == "cellphone"):
                current_connection.device = Cellphone(ip_address=ip_address, connection_instance=command)
            elif(device == "esp"):
                current_connection.esp32 = Esp32(ip_address=ip_address, connection_instance=command)

        else:
            server_log.write(f"A new connection with UUID: {device_uuid} is being created.", "info")
            server_log.write(f"Device type: {device}.", "info")
            if(device == "cellphone"):
                connections.append(Connection(connection_uuid=device_uuid, esp32=None, device=Cellphone(ip_address=ip_address, connection_instance=command)))
            elif(device == "esp"):
                connections.append(Connection(connection_uuid=device_uuid, esp32=Esp32(ip_address=ip_address, connection_instance=command)), device=None)

        server_log.end()
        return 200 

        
        
api.add_resource(StartConnection, "/connect")

if __name__ == "__main__":
    app.run(debug=True)