from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import asyncio
from db_management import *

app = FastAPI()

current_table_name = "test_table"

@app.post("/game-results")
async def receive_game_results(guesses: int):
    global current_table_name, DB_PATH

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print(cursor.execute("SELECT COUNT(*) FROM game_data WHERE name_of_table = '" + current_table_name + "'").fetchall())

    if cursor.execute("SELECT COUNT(*) FROM game_data WHERE name_of_table = '" + current_table_name + "'").fetchall()[0][0] == 0:
        print("Test: " + "INSERT INTO game_data VALUES ('" + current_table_name + "'" + (", 0"*10) + ")")
        cursor.execute("INSERT INTO game_data VALUES ('" + current_table_name + "'" + (", 0"*10) + ")")
    
    if guesses < 10:
        cursor.execute("UPDATE game_data SET in_" + str(guesses) + " = in_" + str(guesses) + " + 1 WHERE name_of_table = '" + current_table_name + "'")
    else:
        cursor.execute("UPDATE game_data SET in_10 = in_10 + 1 WHERE name_of_table = '" + current_table_name + "'")

    resp = cursor.execute("SELECT * FROM game_data WHERE name_of_table = '" + current_table_name + "'").fetchall()[0]

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