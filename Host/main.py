from google import genai
from google.genai import types
from config import API_KEY_GEMINI
from mcp_client import mcp_client
import time
import json
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph, END
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# Define the function declaration for the model

class hostAI:
    def __init__(self):
        self.client = genai.Client(api_key=API_KEY_GEMINI)
        self.listTool = dict()
        self.tools_list = []
        self.workflow = StateGraph(state_schema=MessagesState)
        self.message_history = []

    def subscribeTool(self, tool_name, tool_description, tool_address):
        client = mcp_client(tool_name, tool_description, tool_address)
        self.listTool[tool_name] = client
        
        client.connect()
        time.sleep(1)

        client.discover()
        tools = client.getToolsInfo()
        self.tools_list += tools


    def function_calling_excution(self, function_name, arguments):
        client = self.listTool[function_name.split('_')[0]]
        functionName = function_name[function_name.index('_') + 1:]
        # print(functionName, arguments)
        data = client.function_calling(functionName, arguments)
        return data

    def call_model(self, state: MessagesState):

        tools = types.Tool(function_declarations=self.tools_list)
        config = types.GenerateContentConfig(tools=[tools])
        # print(state["messages"])
        previous_message = state["messages"][:-1]
        last_human_message_history = ''
        if len(previous_message) >= 2:
            last_human_message_history =  ',' + state["messages"][-1].content 

        # print(last_human_message_history + state["messages"][-1].content)
        response =  self.client.models.generate_content(
                        model="gemini-2.0-flash",
                        contents= state["messages"][-1].content,
                        config=config,
                    )
        

        if response.candidates[0].content.parts[0].function_call:
            function_call = response.candidates[0].content.parts[0].function_call
            data = self.function_calling_excution(function_call.name, function_call.args)
            # response = json.loads(data)
            print(f"Function to call: {function_call.name}")
            print(f"Arguments: {function_call.args}")
            return {
                "messages": state["messages"] + [AIMessage(content=json.dumps(data, ensure_ascii=False))]
            }

        else:
            
            response = {
                'function': 'gemini',
                'data': {
                    'type': "text",
                    'data': response.text
                }
              
            }
            return {
                "messages": state["messages"] + [AIMessage(content=json.dumps(response, ensure_ascii=False))]
            }
        
    def start_app(self):
        self.workflow.add_node("model", self.call_model)
        self.workflow.add_edge(START, "model")
        memory = MemorySaver()
        self.app = self.workflow.compile(checkpointer=memory)

    def chat_app(self, content):
        self.message_history.append(HumanMessage(content=content))
        result = self.app.invoke(
            {"messages": self.message_history },
            config={"configurable": {"thread_id": "1"}},
        )
        self.message_history = result["messages"]
        print(type(json.loads(result["messages"][-1].content)))
        return json.loads(result["messages"][-1].content)


    def chat(self, content):
        tools = types.Tool(function_declarations=self.tools_list)
        config = types.GenerateContentConfig(tools=[tools])

        response =  self.client.models.generate_content(
                        model="gemini-2.0-flash",
                        contents=content,
                        config=config,
                    )
        
        if response.candidates[0].content.parts[0].function_call:
            function_call = response.candidates[0].content.parts[0].function_call
            data = self.function_calling_excution(function_call.name, function_call.args)
            print(f"Function to call: {function_call.name}")
            print(f"Arguments: {function_call.args}")
            print(data)
            return dict(data)
            #  In a real app, you would call your function here:
            #  result = schedule_meeting(**function_call.args)
        else:
            print("No function call found in the response.")
            print(response.text)
            return response.text

            

if __name__ == "__main__":
    chatBot = hostAI()
    chatBot.subscribeTool("ecommerce", "These tools use chat with data in ecommerce", "ws://localhost:8000/ws")
    chatBot.start_app()
    # chatBot.chat_app("I need to get median value in price of woman clothes")
    while True:
        prompt = input()
        chatBot.chat_app(prompt)

    
