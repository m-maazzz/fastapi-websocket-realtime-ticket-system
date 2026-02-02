# 🚀 FastAPI Real-Time Support Ticket Chat

A real-time support ticket and chat system built using **FastAPI WebSockets**.  
The project focuses on **real-time communication, in-memory state management, and UI synchronization** — intentionally built **without a database** to clearly demonstrate WebSocket behavior and system design decisions.

This repository is designed as a **portfolio and learning project**, not a production-ready support platform.

---

## 📌 Project Overview

This system allows users to create support tickets and chat with staff members in real time.  
Staff members can go online or offline, view incoming tickets instantly, and explicitly choose which ticket to handle.

All state is managed **in memory**, making connection handling, presence tracking, and reconnect logic fully visible and easy to reason about.

---

## 🎯 Goals of This Project

This project was built to demonstrate:

- Real-time system design
- WebSocket lifecycle management
- Online / offline presence tracking
- Frontend–backend state synchronization
- UX-aware backend decisions
- Clean separation of concerns

Rather than focusing on CRUD operations or database persistence, the emphasis is on **correct real-time behavior**.

---

## ✨ Features

### 👤 User Side
- Create a support ticket
- Receive a generated **Ticket ID**
- Real-time chat with staff
- System messages for:
  - Ticket created
  - Staff joined
  - Staff went offline
  - Staff reconnected
- Chat input automatically disabled when staff is offline
- Chat resumes smoothly when staff reconnects

---

### 🧑‍💼 Staff Side
- Go **Online / Offline**
- View waiting tickets in real time
- Select a ticket to begin chatting
- Clear visual indicators for:
  - Active ticket
  - Disabled tickets
- Chat closes automatically when staff goes offline
- Tickets remain visible even when staff is offline
- Staff must **explicitly re-pick a ticket after reconnecting**

This behavior is intentional to avoid accidental or misleading chat states.

---

## 🧠 Technical Concepts Demonstrated

- WebSocket connection management
- In-memory state handling
- Presence tracking (online / offline)
- Real-time ticket broadcasting
- UI state synchronization with backend state
- Preventing “ghost messages”
- Correct handling of disconnects and reconnects
- Manager pattern for clean separation of logic

---

## 🏗️ Tech Stack

- **Backend:** FastAPI (Python)
- **Realtime:** WebSockets
- **Frontend:** HTML, CSS, Vanilla JavaScript
- **State Storage:** In-memory Python data structures

---

## 📁 Project Structure

project/
│
├── app/
│ ├── init.py
│ ├── main.py # WebSocket endpoints
│ └── websocket_manager.py # Connection and state manager
│
└── frontend/
├── user.html # User chat UI
└── staff.html # Staff dashboard UI


---

## 🔄 System Flow

1. User connects via WebSocket
2. User creates a support ticket
3. Ticket is stored in memory
4. Online staff receive the ticket instantly
5. Staff selects a ticket → chat begins
6. Messages are exchanged in real time
7. Staff goes offline → user is notified, chat is locked
8. Staff reconnects → must explicitly re-pick the ticket

---

## 🔌 WebSocket Endpoints

### User
/ws/user/{user_id}


### Staff
/ws/staff/{staff_id}


---

## ▶️ Running the Project

### 1️⃣ Start Backend
```bash
uvicorn app.main:app --reload
2️⃣ Open Frontend
Open directly in the browser:

frontend/user.html
frontend/staff.html
No frontend server is required.

⚠️ Intentional Design Limitations
❌ No database

❌ No data persistence after server restart

❌ No chat history storage

Why these limitations exist
These limitations are intentional and documented.

The goal of this project is not to demonstrate persistence or scalability, but to focus on:

WebSocket behavior

Real-time state transitions

Presence awareness

Correct UI synchronization

By removing persistence, the real-time system behavior is easier to reason about and evaluate during code review or interviews.

This is often a positive signal in technical interviews, as it shows conscious trade-off decisions rather than missing features.

🧪 Edge Cases Handled
Staff disconnects during an active chat

User attempts to send messages while staff is offline

Staff reconnects and must re-select a ticket

Tickets are not lost when staff goes offline

UI never displays misleading or stale states

🏆 What This Project Demonstrates
Ability to design real-time systems

Strong understanding of WebSocket lifecycle

Backend–frontend coordination

UX-aware engineering decisions

Clean, readable code organization

Honest and intentional handling of limitations

🔮 Possible Enhancements
Redis or database persistence

Multiple staff assignment

Ticket auto-assignment

Typing indicators

Message timestamps

Authentication & authorization

Dockerized deployment

📝 Note for Reviewers
This project is intentionally scoped to highlight real-time communication and state management rather than persistence or infrastructure concerns.

It is best evaluated as a demonstration of WebSocket-driven system design.