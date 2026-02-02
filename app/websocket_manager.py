# app/websocket_manager.py
from fastapi import WebSocket
from typing import Dict
import json
import uuid

class WebSocketManager:
    def __init__(self):
        self.users: Dict[str, WebSocket] = {}
        self.staff: Dict[str, WebSocket] = {}
        self.staff_status: Dict[str, str] = {}
        self.tickets: Dict[str, dict] = {}
        self.active_chats: Dict[str, dict] = {}

    async def connect_user(self, user_id: str, websocket: WebSocket):
        await websocket.accept()
        self.users[user_id] = websocket

    async def connect_staff(self, staff_id: str, websocket: WebSocket):
        await websocket.accept()
        self.staff[staff_id] = websocket
        self.staff_status[staff_id] = "offline"

    def disconnect_user(self, user_id: str):
        self.users.pop(user_id, None)

    def disconnect_staff(self, staff_id: str):
        self.staff.pop(staff_id, None)
        self.staff_status[staff_id] = "offline"

    async def create_ticket(self, user_id: str):
        ticket_id = str(uuid.uuid4())
        self.tickets[ticket_id] = {
            "ticket_id": ticket_id,
            "user_id": user_id,
            "status": "waiting"
        }

        await self.broadcast_to_online_staff({
            "type": "new_ticket",
            "ticket": self.tickets[ticket_id]
        })

        return ticket_id

    async def broadcast_to_online_staff(self, message: dict):
        for staff_id, ws in self.staff.items():
            if self.staff_status.get(staff_id) == "online":
                await ws.send_text(json.dumps(message))

    async def assign_ticket(self, ticket_id: str, staff_id: str):
        ticket = self.tickets.get(ticket_id)
        if not ticket:
            return False

        ticket["status"] = "assigned"
        self.active_chats[ticket_id] = {
            "user_id": ticket["user_id"],
            "staff_id": staff_id
        }

        # notify user
        user_ws = self.users.get(ticket["user_id"])
        if user_ws:
            await user_ws.send_text(json.dumps({
                "type": "assigned",
                "ticket_id": ticket_id
            }))

        return True


    async def disconnect_staff(self, staff_id: str):
        self.staff.pop(staff_id, None)
        self.staff_status[staff_id] = "offline"

        # notify users whose staff went offline
        for ticket_id, chat in self.active_chats.items():
            if chat["staff_id"] == staff_id:
                user_ws = self.users.get(chat["user_id"])
                if user_ws:
                    await user_ws.send_text(json.dumps({
                        "type": "staff_offline",
                        "ticket_id": ticket_id
                    }))
