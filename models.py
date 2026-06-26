from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    theme = db.Column(db.String(20), default='dark')
    pomodoro_sound = db.Column(db.String(200), default='https://actions.google.com/sounds/v1/alarms/alarm_clock.ogg')
    pomodoro_time = db.Column(db.Integer, default=25)

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    task = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(100))
    deadline = db.Column(db.String(50))
    priority = db.Column(db.String(20), default='Low')
    position = db.Column(db.Integer, default=0)
    done = db.Column(db.Integer, default=0)

class Subtask(db.Model):
    __tablename__ = 'subtasks'
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, nullable=False)
    text = db.Column(db.String(255), nullable=False)
    done = db.Column(db.Integer, default=0)
