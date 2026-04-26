from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import asyncio
from db_management import *

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
current_table_name = "test_table"

@app.post("/game-results")
async def receive_game_results(guesses: int, table_name: str):
    """
    API call done at the end of the daily Omnidle game. 
    Recieves the number of guesses and the table played on. Stores the appropriate data. 
    Then returns the statistics of all players for that table.
    """
    global DB_PATH

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    if cursor.execute("SELECT COUNT(*) FROM game_data WHERE name_of_table = ?", (table_name,)).fetchall()[0][0] == 0:
        cursor.execute("INSERT INTO game_data VALUES ( ?, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)", (table_name,))
    
    if guesses < 10:
        cursor.execute("UPDATE game_data SET in_" + str(guesses) + " = in_" + str(guesses) + " + 1 WHERE name_of_table = ?", (table_name,))
    else:
        cursor.execute("UPDATE game_data SET in_10 = in_10 + 1 WHERE name_of_table = ?", (table_name,))

    resp = cursor.execute("SELECT * FROM game_data WHERE name_of_table = ?", (table_name,)).fetchall()[0]

    conn.commit()
    conn.close()

    return {"status": "success", "global_guesses": resp}



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