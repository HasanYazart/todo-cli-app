from flask import Blueprint, Response, current_app, flash, g, jsonify, redirect, render_template, request, session
import json
import os
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
from models import db, User, Task
from routes import login_required

auth_bp = Blueprint('auth', __name__)

SOUND_CHOICES = {
    'https://actions.google.com/sounds/v1/alarms/alarm_clock.ogg',
    'https://actions.google.com/sounds/v1/alarms/digital_watch_alarm_long.ogg',
    'https://actions.google.com/sounds/v1/alarms/beep_short.ogg',
}
ALLOWED_SOUND_EXTENSIONS = {'mp3', 'ogg', 'wav'}

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("u", "").strip()
        password = request.form.get("p", "")
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session.clear()
            session["user"] = user.id
            return redirect("/")
        flash("Kullanıcı adı veya şifre hatalı.")
    return render_template("login.html")

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("u", "").strip()
        password = request.form.get("p", "")
        if not 3 <= len(username) <= 50:
            flash("Kullanıcı adı 3-50 karakter arasında olmalı.")
            return render_template("register.html"), 400
        if len(password) < 8:
            flash("Şifre en az 8 karakter olmalı.")
            return render_template("register.html"), 400
        try:
            db.session.add(User(username=username, password=generate_password_hash(password)))
            db.session.commit()
            flash("Kayıt başarılı! Şimdi giriş yapabilirsiniz.")
            return redirect("/login")
        except IntegrityError:
            db.session.rollback()
            flash("Bu kullanıcı adı zaten mevcut.")
    return render_template("register.html")

@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    session.clear()
    return redirect("/login")

@auth_bp.route("/profile")
@login_required
def profile():
    return render_template("profile.html", user=g.current_user)

@auth_bp.route("/profile/password", methods=["POST"])
@login_required
def profile_password():
    user = g.current_user
    old_p = request.form.get("old_p", "")
    new_p = request.form.get("new_p", "")
    
    if not check_password_hash(user.password, old_p):
        return jsonify({"status": "error", "message": "Eski şifreniz hatalı."}), 400
    if len(new_p) < 8:
        return jsonify({"status": "error", "message": "Yeni şifre en az 8 karakter olmalı."}), 400

    user.password = generate_password_hash(new_p)
    db.session.commit()
    return jsonify({"status": "success", "message": "Şifreniz başarıyla güncellendi!"})

@auth_bp.route("/profile/export")
@login_required
def profile_export():
    tasks = Task.query.filter_by(user_id=g.current_user.id).order_by(Task.position.asc(), Task.id.asc()).all()
    export_data = []
    for t in tasks:
        export_data.append({
            "task": t.task,
            "category": t.category,
            "deadline": t.deadline,
            "priority": t.priority,
            "done": bool(t.done),
            "subtasks": [{"text": s.text, "done": bool(s.done)} for s in t.subtasks]
        })
        
    json_data = json.dumps(export_data, ensure_ascii=False, indent=2)
    return Response(
        json_data,
        mimetype="application/json",
        headers={"Content-disposition": "attachment; filename=todo_export.json"}
    )

@auth_bp.route("/profile/delete", methods=["POST"])
@login_required
def profile_delete():
    db.session.delete(g.current_user)
    db.session.commit()
    session.clear()
    return jsonify({"status": "success"})

@auth_bp.route("/profile/settings", methods=["POST"])
@login_required
def profile_settings():
    user = g.current_user
    
    theme = request.form.get("theme")
    if theme not in {"dark", "light"}:
        return jsonify({"status": "error", "message": "Geçersiz tema seçimi."}), 400
    user.theme = theme
        
    p_time = request.form.get("pomodoro_time")
    if p_time not in {"15", "25", "30", "45", "60"}:
        return jsonify({"status": "error", "message": "Geçersiz Pomodoro süresi."}), 400
    user.pomodoro_time = int(p_time)
        
    p_sound = request.form.get("pomodoro_sound")
    if p_sound == "custom":
        file = request.files.get("sound_file")
        if file and file.filename:
            ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
            if ext not in ALLOWED_SOUND_EXTENSIONS or not (
                file.mimetype.startswith("audio/") or file.mimetype == "application/ogg"
            ):
                return jsonify({"status": "error", "message": "Sadece MP3, OGG ve WAV yüklenebilir!"}), 400

            upload_dir = os.path.join(current_app.static_folder, "uploads")
            os.makedirs(upload_dir, exist_ok=True)
            for old_ext in ALLOWED_SOUND_EXTENSIONS:
                old_path = os.path.join(upload_dir, f"user_{user.id}_sound.{old_ext}")
                if os.path.exists(old_path):
                    os.remove(old_path)
            filename = secure_filename(f"user_{user.id}_sound.{ext}")
            file.save(os.path.join(upload_dir, filename))
            user.pomodoro_sound = f"/static/uploads/{filename}"
        elif user.pomodoro_sound in SOUND_CHOICES:
            return jsonify({"status": "error", "message": "Lütfen bir ses dosyası seçin."}), 400
    elif p_sound in SOUND_CHOICES:
        user.pomodoro_sound = p_sound
    else:
        return jsonify({"status": "error", "message": "Geçersiz ses seçimi."}), 400
            
    db.session.commit()
    return jsonify({"status": "success", "message": "Ayarlar kaydedildi."})

