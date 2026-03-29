from flask import Flask, render_template, redirect, url_for, request, flash
from flask_socketio import SocketIO, emit
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Message
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'gaurav_final_stable_2026'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
socketio = SocketIO(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- ROUTES ---

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('chat'))
        else:
            flash('Invalid username or password!')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        user_exists = User.query.filter((User.username == username) | (User.email == email)).first()
        if user_exists:
            flash('Username or Email already exists!')
            return redirect(url_for('register'))
            
        hashed_pw = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, email=email, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/chat')
@login_required
def chat():
    all_users = User.query.filter(User.username != current_user.username).all()
    # Private chat filtering logic
    history = Message.query.filter(
        (Message.recipient_id == None) | 
        (Message.sender_id == current_user.id) | 
        (Message.recipient_id == current_user.id)
    ).all()
    return render_template('chat.html', username=current_user.username, history=history, all_users=all_users)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# --- SOCKET EVENTS ---

@socketio.on('message')
def handle_message(data):
    msg_content = data.get('msg')
    target = data.get('recipient') 
    
    recipient_id = None
    if target and target != 'Community Group':
        recipient = User.query.filter_by(username=target).first()
        if recipient:
            recipient_id = recipient.id

    new_msg = Message(
        sender_id=current_user.id,
        recipient_id=recipient_id,
        content=msg_content
    )
    db.session.add(new_msg)
    db.session.commit()

    emit_data = {
        'sender': current_user.username,
        'recipient': target if target else 'Community Group',
        'msg': msg_content,
        'time': datetime.now().strftime('%I:%M %p')
    }
    socketio.emit('message', emit_data)

@socketio.on('typing')
def handle_typing(data):
    # Sends typing status to everyone except the sender
    emit('typing', data, broadcast=True, include_self=False)

# --- SERVER START ---

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    print("\n" + "="*40)
    print("🚀 CLOUD CHAT IS LIVE!")
    print("👉 URL: http://127.0.0.1:5000")
    print("="*40 + "\n")
    
    # use_reloader=False prevents the infinite restarting loop on Windows
    socketio.run(app, debug=True, use_reloader=False, port=5000)