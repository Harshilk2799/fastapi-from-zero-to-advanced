from fastapi import FastAPI, BackgroundTasks

import time 
app = FastAPI()

def write_notification(email: str, message: str = ""):
    time.sleep(50)
    with open("log.txt", mode="w") as email_file:
        content = f"notification for {email} : {message}"
        email_file.write(content)

@app.post("/send-notification/{email}")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_notification, email, message="Some notification by harshil")
    return {"message": "Notification send!"}