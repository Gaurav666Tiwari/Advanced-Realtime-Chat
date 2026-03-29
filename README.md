# 🚀 Advanced Real-Time Chat Application

A high-performance, real-time messaging platform built with **Python (Flask)** and **Socket.io**. This application supports private messaging, community group chats, and features a premium dark-themed UI inspired by modern developer aesthetics.

## ✨ Key Features
* **Real-time Messaging:** Instant message delivery using WebSockets via Flask-SocketIO.
* **Private & Group Chat:** Seamlessly switch between private one-on-one conversations and a global community group.
* **Typing Indicators:** Real-time visual feedback when other users are typing.
* **Smart Audio Notifications:** iPhone-style "Ding" sound notifications for incoming messages.
* **Unread Message Badges:** Dynamic badges in the sidebar to track missed messages from different users.
* **Secure Authentication:** Robust login and registration system using hashed passwords (Werkzeug).
* **Premium UI/UX:** Responsive design with 'Plus Jakarta Sans' typography and a custom CSS scrollbar.

## 🛠️ Tech Stack
* **Backend:** Python 3.11, Flask
* **Real-time Engine:** Flask-SocketIO
* **Database:** SQLite with SQLAlchemy ORM
* **Frontend:** HTML5, CSS3 (Custom Variables), JavaScript (Vanilla)
* **Session Management:** Flask-Login

## 📸 Project Structure
```text
D:\advanced_chat_app\
├── static/
│   ├── sounds/ (Notification mp3)
│   └── style.css
├── templates/
│   ├── chat.html
│   ├── login.html
│   └── register.html
├── app.py (Main Server)
├── models.py (Database Schema)
└── requirements.txt
🚀 How to Run Locally
Clone the repository:

Bash
git clone [https://github.com/Gaurav666Tiwari/Advanced-Realtime-Chat.git](https://github.com/Gaurav666Tiwari/Advanced-Realtime-Chat.git)
Navigate to the folder:

Bash
cd Advanced-Realtime-Chat
Install dependencies:

Bash
pip install -r requirements.txt
Run the application:

Bash
python app.py
Access the app: Open http://127.0.0.1:5000 in your browser.
