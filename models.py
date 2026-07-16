from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from sqlalchemy.engine import Engine


@event.listens_for(Engine, "connect")
def enable_sqlite_foreign_keys(dbapi_connection, _connection_record):
    """Make SQLite enforce the foreign keys declared below."""
    if dbapi_connection.__class__.__module__.startswith("sqlite3"):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    theme = db.Column(db.String(20), default='dark')
    pomodoro_sound = db.Column(db.String(200), default='https://actions.google.com/sounds/v1/alarms/alarm_clock.ogg')
    pomodoro_time = db.Column(db.Integer, default=25)
    tasks = db.relationship('Task', back_populates='user', cascade='all, delete-orphan')

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    task = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(100))
    deadline = db.Column(db.String(50))
    priority = db.Column(db.String(20), default='Low')
    position = db.Column(db.Integer, default=0)
    done = db.Column(db.Integer, default=0)
    user = db.relationship('User', back_populates='tasks')
    subtasks = db.relationship('Subtask', back_populates='task', cascade='all, delete-orphan')

class Subtask(db.Model):
    __tablename__ = 'subtasks'
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id', ondelete='CASCADE'), nullable=False)
    text = db.Column(db.String(255), nullable=False)
    done = db.Column(db.Integer, default=0)
    task = db.relationship('Task', back_populates='subtasks')
