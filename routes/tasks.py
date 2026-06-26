from flask import Blueprint, render_template, request, redirect, session, jsonify
from datetime import datetime
from models import db, Task, Subtask, User

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route("/", methods=["GET"])
def home():
    if "user" not in session:
        return redirect("/login")
        
    user = User.query.get(session["user"])

    tasks = Task.query.filter_by(user_id=session["user"]).order_by(Task.position.asc(), Task.id.asc()).all()
    data = []
    
    for t in tasks:
        subs = Subtask.query.filter_by(task_id=t.id).all()
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
            except:
                pass
                
        data.append({"task": t, "subs": subs, "p": percent, "rem": rem})

    return render_template("index.html", tasks=data, user=user)

@tasks_bp.route("/add", methods=["POST"])
def add():
    new_task = Task(
        user_id=session["user"],
        task=request.form["task"],
        category=request.form["category"],
        deadline=request.form["deadline"],
        priority=request.form.get("priority", "Low")
    )
    db.session.add(new_task)
    db.session.commit()
    return redirect("/")

@tasks_bp.route("/edit/<int:id>", methods=["POST"])
def edit(id):
    t = Task.query.get_or_404(id)
    t.task = request.form["task"]
    t.category = request.form["category"]
    t.deadline = request.form["deadline"]
    t.priority = request.form.get("priority", "Low")
    db.session.commit()
    return redirect("/")

@tasks_bp.route("/add_sub/<int:id>", methods=["POST"])
def add_sub(id):
    db.session.add(Subtask(task_id=id, text=request.form["text"]))
    db.session.commit()
    return redirect("/")

@tasks_bp.route("/api/done/<int:id>", methods=["POST"])
def api_done(id):
    t = Task.query.get_or_404(id)
    t.done = 1 - t.done
    db.session.commit()
    return jsonify({"status": "success", "is_done": t.done})

@tasks_bp.route("/api/delete/<int:id>", methods=["POST"])
def api_delete(id):
    Subtask.query.filter_by(task_id=id).delete()
    Task.query.filter_by(id=id).delete()
    db.session.commit()
    return jsonify({"status": "success"})

@tasks_bp.route("/api/toggle/<int:id>", methods=["POST"])
def api_toggle(id):
    sub = Subtask.query.get_or_404(id)
    sub.done = 1 - sub.done
    db.session.commit()
    
    subs = Subtask.query.filter_by(task_id=sub.task_id).all()
    total = len(subs)
    done_count = len([s for s in subs if s.done == 1])
    percent = int((done_count / total) * 100) if total else 0
        
    return jsonify({"status": "success", "is_done": sub.done, "percent": percent})

@tasks_bp.route("/api/reorder", methods=["POST"])
def api_reorder():
    order = request.json.get("order", [])
    for idx, task_id in enumerate(order):
        t = Task.query.get(task_id)
        if t and t.user_id == session.get("user"):
            t.position = idx
    db.session.commit()
    return jsonify({"status": "success"})
