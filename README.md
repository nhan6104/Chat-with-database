# Gemini Function Calling Host

This project is a function-calling host powered by Google's Gemini API. It allows you to integrate tools over WebSocket using the `mcp_client`, discover their functions, and dynamically invoke them via AI-generated function calls.

## Features

- 🌐 **Tool Discovery via WebSocket**: Dynamically connect and register external tools.
- 🧠 **Gemini 2.0 Flash Integration**: Uses Google's latest model for intelligent message processing and function calling.
- 🔁 **Function Calling Workflow**: Automatically handles tool invocation based on model output.
- 🗂️ **Memory-based Message Tracking**: Tracks chat history using `langgraph`.

## Project Structure

- `main.py`: Main controller that initializes Gemini client, connects tools, and handles AI chat and function execution.
- `mcp_client.py`: WebSocket client to connect with external tools, handle messages, and send/receive function call data.
- `config.py`: Contains your Gemini API key.

## Installation

1. **Clone the Repository**

```bash
https://github.com/nhan6104/Chat_with_database.git
```

2. **Install Dependencies**

```bash
pip install -r requirement.txt
```

3. **Configure Your API Key**

Edit `config.py` and replace the dummy key with your actual API key:

```python
API_KEY_GEMINI = "your_actual_api_key"
```

## Usage

Start your tool server at the WebSocket address (e.g., `ws://localhost:8000/ws`), then run the chatbot:

```bash
cd Host
streamlit run ui.py
```

Enter your message, and if the AI determines a tool function is needed, it will call it automatically.

## Example

```
> I need to get median value in price of woman clothes
Function to call: ecommerce_get_median_value
Arguments: None
{'type': 'number', 'data': 42.5}
```

## Notes

- Make sure your external tool is WebSocket-enabled and supports the `discover` protocol and function execution.
- Each tool function must respond in a predefined format.

## License

MIT License


## Running the WebSocket Tool Server

Your Gemini host connects to external tools via WebSocket. You can use the provided tool server by running:

```bash
cd ecommerceDatabase_Server
python mcp_server.py
```

Make sure the `product.csv` file is present in the same directory, as it's required for data loading and tool definitions.

This server exposes several analytical tools, including:

- `get_median_value`
- `get_unique_values`
- `get_empty_values`
- `get_max_values`
- `describeColumn`
- `get_correlation`
- ...

These are auto-discovered and registered by the host.

## Example Connection Flow

1. Run the tool server:

```bash
python mcp_server.py
```

2. In a new terminal, start the host:

```bash
python main.py
```

3. Type a message like:

```
Give me the median price of woman clothing.
```

The system will:

- Send message to Gemini model
- Model calls a relevant function (e.g., `ecommerce_get_median_value`)
- Host routes that call to the tool server via WebSocket
- Tool responds with calculated result
- Result is printed and returned as chat response
