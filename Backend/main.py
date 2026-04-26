from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import asyncio

app = FastAPI()

# Allow the Vite dev server to make cross-origin requests to this API.
# Without this the browser blocks all HTTP responses from a different origin.
# WebSocket connections are not subject to CORS but use the same origin allowlist
# via the browser's Upgrade handshake Origin header.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple HTML page for testing WebSocket
html = """
<!DOCTYPE html>
<html>
    <head>
        <title>WebSocket Test</title>
    </head>
    <body>
        <h1>WebSocket Test</h1>
        <div id="messages"></div>
        <script>
            const ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                const messages = document.getElementById('messages');
                messages.innerHTML += '<p>' + event.data + '</p>';
            };
            ws.onopen = function(event) {
                console.log("WebSocket opened");
            };
        </script>
    </body>
</html>
"""

@app.get("/health")
async def health():
    # Polled by the Docker daemon for container health monitoring
    return {"status": "ok"}

@app.get("/")
async def get():
    return HTMLResponse(html)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        # Simulate sending data to frontend
        data = "Hello from backend!"
        await websocket.send_text(data)
        await asyncio.sleep(5)  # Send every 5 seconds