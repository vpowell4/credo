from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = FastAPI(title="My MCP Server", version="1.0.0")

API_KEY = os.getenv("MCP_API_KEY", "my_secret_token")

# Middleware to check Bearer token
@app.middleware("http")
async def verify_api_key(request: Request, call_next):
    auth_header = request.headers.get("Authorization")
    if not auth_header or auth_header != f"Bearer {API_KEY}":
        return JSONResponse(status_code=401, content={"error": "Unauthorized"})
    return await call_next(request)

# Health check
@app.get("/")
def health_check():
    return {"status": "ok", "name": "My MCP Server"}

# Tool 1: Echo
@app.post("/echo")
async def echo(data: dict):
    return {"received": data, "message": "Echo from MCP server!"}

# Tool 2: Hello
@app.get("/hello")
def say_hello(name: str = "Agent"):
    return {"message": f"Hello, {name}! Greetings from your MCP server."}

# MCP tool discovery endpoint
@app.get("/tools")
def list_tools():
    return {
        "tools": [
            {
                "name": "echo",
                "description": "Echoes back the received input",
                "method": "POST",
                "path": "/echo",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "message": {"type": "string", "description": "Message to echo"}
                    },
                    "required": ["message"]
                },
            },
            {
                "name": "hello",
                "description": "Greets the user by name",
                "method": "GET",
                "path": "/hello",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Name to greet"}
                    },
                    "required": []
                },
            },
        ]
    }
