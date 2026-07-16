from flask import Blueprint, flash, g, jsonify, redirect, render_template, request, session
from datetime import datetime
from sqlalchemy import func
from models import db, Task, Subtask, User
from routes import login_required

tasks_bp = Blueprint('tasks', __name__)

PRIORITIES = {"Low", "Medium", "High"}


def task_form_data():
    text = request.form.get("task", "").strip()
    category = request.form.get("category", "").strip()
    deadline = request.form.get("deadline", "").strip()
    priority = request.form.get("priority", "Low")

    if not text or len(text) > 255:
        return None, "Görev 1-255 karakter arasında olmalı."
    if len(category) > 100:
        return None, "Kategori en fazla 100 karakter olabilir."
    if priority not in PRIORITIES:
        return None, "Geçersiz öncelik seçimi."
    if deadline:
        try:
            datetime.strptime(deadline, "%Y-%m-%d")
        except ValueError:
            return None, "Geçersiz tarih."
    return {"task": text, "category": category, "deadline": deadline, "priority": priority}, None


def owned_task_or_404(task_id):
    return Task.query.filter_by(id=task_id, user_id=g.current_user.id).first_or_404()

@tasks_bp.route("/", methods=["GET"])
@login_required
def home():
    tasks = Task.query.filter_by(user_id=g.current_user.id).order_by(Task.position.asc(), Task.id.asc()).all()
    data = []
    
    for t in tasks:
        subs = t.subtasks
        total = len(subs)
        done_count = len([s for s in subs if s.done == 1])
        percent = int((done_count / total) * 100) if total else 0
        
        rem = ""
        if t.deadline:
            try:
                delta = datetime.strptime(t.deadline, "%Y-%m-%d").date() - datetime.today().date()
                if delta.days > 0: rem = f"{delta.days} gün kaldı"
                elif delta.days == 0: rem = "Bugün"
                else: rem = "Geçti"
            except ValueError:
                pass
                
        data.append({"task": t, "subs": subs, "p": percent, "rem": rem})

    return render_template("index.html", tasks=data, user=g.current_user)

@tasks_bp.route("/add", methods=["POST"])
@login_required
def add():
    values, error = task_form_data()
    if error:
        flash(error)
        return redirect("/")
    last_position = db.session.query(func.max(Task.position)).filter_by(user_id=g.current_user.id).scalar() or 0
    new_task = Task(
        user_id=g.current_user.id,
        position=last_position + 1,
        **values,
    )
    db.session.add(new_task)
    db.session.commit()
    return redirect("/")

@tasks_bp.route("/edit/<int:id>", methods=["POST"])
@login_required
def edit(id):
    t = owned_task_or_404(id)
    values, error = task_form_data()
    if error:
        flash(error)
        return redirect("/")
    for key, value in values.items():
        setattr(t, key, value)
    db.session.commit()
    return redirect("/")

@tasks_bp.route("/add_sub/<int:id>", methods=["POST"])
@login_required
def add_sub(id):
    task = owned_task_or_404(id)
    text = request.form.get("text", "").strip()
    if not text or len(text) > 255:
        flash("Alt görev 1-255 karakter arasında olmalı.")
        return redirect("/")
    db.session.add(Subtask(task_id=task.id, text=text))
    db.session.commit()
    return redirect("/")

@tasks_bp.route("/api/done/<int:id>", methods=["POST"])
@login_required
def api_done(id):
    t = owned_task_or_404(id)
    t.done = 1 - t.done
    db.session.commit()
    return jsonify({"status": "success", "is_done": t.done})

@tasks_bp.route("/api/delete/<int:id>", methods=["POST"])
@login_required
def api_delete(id):
    task = owned_task_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({"status": "success"})

@tasks_bp.route("/api/toggle/<int:id>", methods=["POST"])
@login_required
def api_toggle(id):
    sub = (
        Subtask.query.join(Task)
        .filter(Subtask.id == id, Task.user_id == g.current_user.id)
        .first_or_404()
    )
    sub.done = 1 - sub.done
    db.session.commit()
    
    subs = sub.task.subtasks
    total = len(subs)
    done_count = len([s for s in subs if s.done == 1])
    percent = int((done_count / total) * 100) if total else 0
        
    return jsonify({"status": "success", "is_done": sub.done, "percent": percent})

@tasks_bp.route("/api/reorder", methods=["POST"])
@login_required
def api_reorder():
    payload = request.get_json(silent=True) or {}
    order = payload.get("order", [])
    if not isinstance(order, list) or not all(isinstance(task_id, int) and task_id > 0 for task_id in order):
        return jsonify({"status": "error", "message": "Geçersiz sıralama verisi."}), 400
    for idx, task_id in enumerate(order):
        t = db.session.get(Task, task_id)
        if t and t.user_id == g.current_user.id:
            t.position = idx
    db.session.commit()
    return jsonify({"status": "success"})
