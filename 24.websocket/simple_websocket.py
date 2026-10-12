from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

app = FastAPI()

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
                var ws = new WebSocket(`ws://localhost:8001/ws`);
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


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message text was: {data}")
    except WebSocketDisconnect:
        print("Client disconnected!") 