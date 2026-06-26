from flask import Blueprint, render_template, request, redirect, session, flash, jsonify, Response
import json
import os
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
from models import db, User, Task, Subtask

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(username=request.form["u"]).first()
        if user and check_password_hash(user.password, request.form["p"]):
            session["user"] = user.id
            return redirect("/")
        flash("Hatalı!")
    return render_template("login.html")

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        try:
            db.session.add(User(username=request.form["u"], password=generate_password_hash(request.form["p"])))
            db.session.commit()
            flash("Başarılı!")
            return redirect("/login")
        except IntegrityError:
            db.session.rollback()
            flash("Mevcut!")
    return render_template("register.html")

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@auth_bp.route("/profile")
def profile():
    if "user" not in session:
        return redirect("/login")
    user = User.query.get(session["user"])
    return render_template("profile.html", user=user)

@auth_bp.route("/profile/password", methods=["POST"])
def profile_password():
    if "user" not in session:
        return jsonify({"status": "error", "message": "Giriş yapmalısınız"}), 403
    
    user = User.query.get(session["user"])
    old_p = request.form.get("old_p")
    new_p = request.form.get("new_p")
    
    if not check_password_hash(user.password, old_p):
        return jsonify({"status": "error", "message": "Eski şifreniz hatalı"})
        
    user.password = generate_password_hash(new_p)
    db.session.commit()
    return jsonify({"status": "success", "message": "Şifreniz başarıyla güncellendi!"})

@auth_bp.route("/profile/export")
def profile_export():
    if "user" not in session:
        return redirect("/login")
        
    tasks = Task.query.filter_by(user_id=session["user"]).order_by(Task.position.asc(), Task.id.asc()).all()
    export_data = []
    for t in tasks:
        subs = Subtask.query.filter_by(task_id=t.id).all()
        export_data.append({
            "task": t.task,
            "category": t.category,
            "deadline": t.deadline,
            "priority": t.priority,
            "done": bool(t.done),
            "subtasks": [{"text": s.text, "done": bool(s.done)} for s in subs]
        })
        
    json_data = json.dumps(export_data, ensure_ascii=False, indent=2)
    return Response(
        json_data,
        mimetype="application/json",
        headers={"Content-disposition": "attachment; filename=todo_export.json"}
    )

@auth_bp.route("/profile/delete", methods=["POST"])
def profile_delete():
    if "user" not in session:
        return jsonify({"status": "error", "message": "Giriş yapmalısınız"}), 403
        
    user_id = session["user"]
    tasks = Task.query.filter_by(user_id=user_id).all()
    for t in tasks:
        Subtask.query.filter_by(task_id=t.id).delete()
    Task.query.filter_by(user_id=user_id).delete()
    User.query.filter_by(id=user_id).delete()
    db.session.commit()
    
    session.clear()
    return jsonify({"status": "success"})

@auth_bp.route("/profile/settings", methods=["POST"])
def profile_settings():
    if "user" not in session:
        return jsonify({"status": "error", "message": "Giriş yapmalısınız"}), 403
        
    user = User.query.get(session["user"])
    
    theme = request.form.get("theme")
    if theme in ["dark", "light"]:
        user.theme = theme
        
    p_time = request.form.get("pomodoro_time")
    if p_time and p_time.isdigit():
        user.pomodoro_time = int(p_time)
        
    p_sound = request.form.get("pomodoro_sound")
    if p_sound:
        if p_sound == "custom":
            if "sound_file" in request.files:
                file = request.files["sound_file"]
                if file and file.filename != "":
                    ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
                    if ext in ['mp3', 'ogg', 'wav']:
                        # Save file
                        filename = secure_filename(f"user_{user.id}_sound.{ext}")
                        filepath = os.path.join("static", "uploads", filename)
                        file.save(filepath)
                        user.pomodoro_sound = "/" + filepath.replace("\\", "/")
                    else:
                        return jsonify({"status": "error", "message": "Sadece MP3, OGG ve WAV yüklenebilir!"})
        else:
            user.pomodoro_sound = p_sound
            
    db.session.commit()
    return jsonify({"status": "success", "message": "Ayarlar kaydedildi."})

