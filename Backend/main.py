from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import asyncio

app = FastAPI()

@app.post("/game-results")
async def receive_game_results(guesses: int):
    return {
        "status": "success",
        "guesses_received": guesses,
        "result_message": f"You made {guesses} guesses!"
    }

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