from fastapi import FastAPI, WebSocket
import uvicorn
import json
from tool_description import get_correlation, get_min_value, get_median_value, get_unique_values, get_empty_values, get_nonempty_values, get_max_values, get_unique_values, get_mean_values, dataframe, describe_column
import sys
from service import toolAnalysis


 

tools = toolAnalysis(dataframe)

app = FastAPI()

# {function: "", arguments: {}}
def handle_request(request):
    print(request)
    if request['function'] == 'discover':
        return [get_correlation, describe_column, get_min_value, get_median_value, get_unique_values, get_empty_values, get_nonempty_values, get_max_values, get_unique_values, get_mean_values]
    
    else:
        f = getattr(tools, request['function'])
        arguments = request.get('arguments') if request.get('arguments') != None else {}
        return f(**arguments)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        request = json.loads(data)

        data = handle_request(request)

        response = {
            "function": request['function'],
            "data": data
        }

        await websocket.send_text(json.dumps(response))

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)