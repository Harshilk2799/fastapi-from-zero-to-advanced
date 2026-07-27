from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from typing import List

app = FastAPI()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    async def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    # async def broadcast(self, message: str):
    #     for connection in self.active_connections:
    #         await connection.send_text(message)

    async def broadcast(self, message: str):
        dead = []
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except RuntimeError:
                dead.append(connection)
        for connection in dead:
            self.active_connections.remove(connection)

manager = ConnectionManager()

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    await manager.broadcast(f"Client #{client_id} joined the chat")
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Client #{client_id}: {data}")
    except WebSocketDisconnect:
        await manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")


# Simple HTML test client served at root
@app.get("/")
async def get():
    html = """
    <!DOCTYPE html>
    <html>
        <head><title>WebSocket Test</title></head>
        <body>
            <h1>WebSocket Chat</h1>
            <input type="text" id="messageText" autocomplete="off"/>
            <button onclick="sendMessage(event)">Send</button>
            <ul id='messages'></ul>
            <script>
                var client_id = Date.now();
                var ws = new WebSocket(`ws://localhost:7877/ws/${client_id}`);
                ws.onmessage = function(event) {
                    var messages = document.getElementById('messages');
                    var message = document.createElement('li');
                    message.textContent = event.data;
                    messages.appendChild(message);
                };
                function sendMessage(event) {
                    var input = document.getElementById("messageText");
                    ws.send(input.value);
                    input.value = '';
                    event.preventDefault();
                }
            </script>
        </body>
    </html>
    """
    return HTMLResponse(html)