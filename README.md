🧑‍💻 Real-Time Support Ticket Chat (FastAPI + WebSockets)

A real-time support ticket and chat system built using FastAPI WebSockets, designed without any database to demonstrate in-memory state management, WebSocket communication, and UI state synchronization.

This project is ideal for showcasing real-time system design, WebSocket handling, and frontend-backend coordination in a portfolio.

🚀 Features
👤 User Side

Create a support ticket

View generated Ticket ID

Real-time chat with staff

Clear system messages:

Ticket created

Staff joined

Staff went offline

Staff reconnected

Chat input automatically disabled when staff is offline

Smooth chat resume when staff reconnects

🧑‍💼 Staff Side

Go Online / Offline

View list of waiting tickets

Pick a ticket to start chat

Clear visual indicator for:

Active ticket

Disabled tickets

Chat closes automatically when going offline

Tickets remain visible even when offline

Must explicitly re-pick ticket after reconnect (intentional UX)

🧠 Key Technical Concepts Demonstrated

WebSocket connection management

In-memory state handling (no database)

Online / offline presence tracking

Real-time ticket broadcasting

UI state synchronization with backend state

Preventing “ghost messages”

Handling reconnects correctly

Separation of concerns (manager pattern)

🏗️ Tech Stack

Backend: FastAPI (Python)

Realtime: WebSockets

Frontend: HTML, CSS, Vanilla JavaScript

State Storage: In-memory Python data structures

📁 Project Structure
project/
│
├── app/
│   ├── __init__.py
│   ├── main.py                # WebSocket endpoints
│   └── websocket_manager.py   # Connection & state manager
│
└── frontend/
    ├── user.html              # User chat UI
    └── staff.html             # Staff dashboard UI

🔄 How It Works (Flow)
Ticket Lifecycle

User connects via WebSocket

User creates a ticket

Ticket is stored in memory

Online staff receive the ticket instantly

Staff picks ticket → chat starts

Messages flow in real time

Staff goes offline → user notified, chat locked

Staff comes back online → must re-pick ticket

🔌 WebSocket Endpoints
User
/ws/user/{user_id}

Staff
/ws/staff/{staff_id}

▶️ Running the Project
1️⃣ Start Backend
uvicorn app.main:app --reload

2️⃣ Open Frontend

Open these files directly in your browser:

frontend/user.html

frontend/staff.html

(No frontend server required)

⚠️ Important Design Notes (Intentional)

❌ No database is used

❌ No data persistence after server restart

❌ No chat history storage

Why?

This project focuses on learning and demonstrating WebSocket behavior and real-time state handling, not persistence.

These limitations are intentional and documented, which is a positive signal in interviews.

🧪 Edge Cases Handled

Staff disconnects while chatting

User tries to send messages when staff offline

Staff reconnects and must re-enter ticket

Tickets not lost when staff goes offline

UI does not show misleading states

🏆 What This Project Shows

Ability to design real-time systems

Understanding of WebSocket lifecycle

Frontend-backend synchronization

UX-aware engineering decisions

Clean separation of logic

Honest handling of limitations

🔮 Possible Enhancements

Redis or database persistence

Multiple staff assignment logic

Ticket auto-assignment

Typing indicators

Message timestamps

Authentication

Deployment with Docker




A real-time support ticket chat system built using FastAPI WebSockets. The project demonstrates live ticket assignment, online/offline presence handling, and UI state synchronization using in-memory data structures without a database.