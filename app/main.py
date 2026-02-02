# app/main.py
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import json
from app.websocket_manager import WebSocketManager

app = FastAPI()
manager = WebSocketManager()

# ---------------- USER SOCKET ----------------
@app.websocket("/ws/user/{user_id}")
async def user_ws(websocket: WebSocket, user_id: str):
    await manager.connect_user(user_id, websocket)

    try:
        while True:
            data = await websocket.receive_text()
            payload = json.loads(data)

            if payload["type"] == "create_ticket":
                ticket_id = await manager.create_ticket(user_id)
                await websocket.send_text(json.dumps({
                    "type": "ticket_created",
                    "ticket_id": ticket_id
                }))

            elif payload["type"] == "message":
                ticket_id = payload["ticket_id"]
                chat = manager.active_chats.get(ticket_id)
                if not chat:
                    continue

                staff_id = chat["staff_id"]

                if manager.staff_status.get(staff_id) != "online":
                    await websocket.send_text(json.dumps({
                        "type": "system",
                        "text": "Staff is offline. Please wait..."
                    }))
                    continue

                staff_ws = manager.staff.get(staff_id)
                if staff_ws:
                    await staff_ws.send_text(json.dumps({
                        "type": "message",
                        "from": "user",
                        "text": payload["text"]
                    }))

    except WebSocketDisconnect:
        manager.disconnect_user(user_id)

# ---------------- STAFF SOCKET ----------------
@app.websocket("/ws/staff/{staff_id}")
async def staff_ws(websocket: WebSocket, staff_id: str):
    await manager.connect_staff(staff_id, websocket)

    try:
        while True:
            data = await websocket.receive_text()
            payload = json.loads(data)

            if payload["type"] == "status":
                new_status = payload["status"]
                manager.staff_status[staff_id] = new_status
                notified_users = set()

                if new_status == "online":
                    for ticket_id, ticket in manager.tickets.items():
                        if ticket["status"] == "waiting":
                            await websocket.send_text(json.dumps({
                                "type": "new_ticket",
                                "ticket": ticket
                            }))

                

                if new_status == "offline":

                    for ticket_id, chat in manager.active_chats.items():
                        if chat["staff_id"] == staff_id:
                            user_id = chat["user_id"]

                            if user_id in notified_users:
                                continue

                            notified_users.add(user_id)

                            user_ws = manager.users.get(user_id)
                            if user_ws:
                                await user_ws.send_text(json.dumps({
                                    "type": "staff_offline"
                                }))

                await websocket.send_text(json.dumps({
                    "type": "status_updated",
                    "status": payload["status"]
                }))

            elif payload["type"] == "pick_ticket":
                success = await manager.assign_ticket(
                    payload["ticket_id"],
                    staff_id
                )
                await websocket.send_text(json.dumps({
                    "type": "ticket_picked",
                    "success": success
                }))

            elif payload["type"] == "message":
                if manager.staff_status.get(staff_id) != "online":
                    continue

                ticket_id = payload["ticket_id"]
                chat = manager.active_chats.get(ticket_id)
                if chat:
                    user_ws = manager.users.get(chat["user_id"])
                    if user_ws:
                        await user_ws.send_text(json.dumps({
                            "type": "message",
                            "from": "staff",
                            "text": payload["text"]
                        }))

    except WebSocketDisconnect:
        manager.disconnect_staff(staff_id)


@app.get("/")
def health():
    return {"status": "WebSocket server running"}