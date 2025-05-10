import threading
import time
import websocket 
import rel 
import json

class mcp_client:
    def __init__(self, clientName, description, websockt_address):
        self.client_name = clientName
        self.ws = websocket.WebSocketApp(websockt_address, 
                              on_open=self.on_open,
                              on_message=self.on_message,
                              on_error=self.on_error,
                              on_close=self.on_close)
        
        self.tools = list()
        self.description = description
        self.isConnected = False
        self.current_command = None
        self.response_event = threading.Event()
        self.response_data = None
    
    def connect(self):
        threading.Thread(target=self._run_ws, daemon=True).start()

    def _run_ws(self):
        self.ws.run_forever(reconnect=5)
       
    def on_message(self, ws, message):
        data = json.loads(message)
        if data['function'] == 'discover':
            for el in data["data"]:
                el["name"] = self.client_name + '_' + el["name"]
                el["description"] = self.description + '.' +  el["description"]
                self.tools.append(el)
        
        else:
            self.response_data = data
            self.response_event.set()

            
    def on_error(self, ws, error):
        print(f"[Error]: {error}")

    def on_close(self, ws, close_status_code, close_msg):
        print("### closed ###")

    def on_open(self, ws):
        print("Opened connection")
        self.isConnected = True

    def send_and_await(self, request):
        self.response_event.clear()
        self.response_data = None

        self.ws.send(request)
        self.response_event.wait(timeout=5)
        return self.response_data
    

    def discover(self):
        request = {
            "function": "discover",
            "arguments": None
        }
        self.ws.send(json.dumps(request))
        time.sleep(2)


    def function_calling(self, function_name, arguments = None):
        request = {
            "function": function_name,
            "arguments": arguments
        }

        data =  self.send_and_await(json.dumps(request))
        return data


    def getToolsInfo(self):
        return self.tools

if __name__ == "__main__":
    client = mcp_client("hello", "jsdhajkasdhask", "ws://localhost:8000/ws")

    # Chạy kết nối trong thread riêng
    client.connect()

    time.sleep(1)  # đợi 1s để kết nối WebSocket thành công

    # Sau đó mới chạy discover
    data = client.function_calling("get_median_value", None)
