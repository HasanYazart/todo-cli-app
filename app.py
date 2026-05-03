# Kütüphaneler
from flask import Flask, render_template, request, redirect, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
from datetime import datetime

# Ayarlar
app = Flask(__name__)
app.secret_key = "secret123"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modeller
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    task = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(100))
    deadline = db.Column(db.String(50))
    done = db.Column(db.Integer, default=0)

class Subtask(db.Model):
    __tablename__ = 'subtasks'
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, nullable=False)
    text = db.Column(db.String(255), nullable=False)
    done = db.Column(db.Integer, default=0)

# Veritabanı
with app.app_context():
    db.create_all()

# Anasayfa
@app.route("/", methods=["GET"])
def home():
    if "user" not in session:
        return redirect("/login")

    tasks = Task.query.filter_by(user_id=session["user"]).all()
    data = []
    
    for t in tasks:
        subs = Subtask.query.filter_by(task_id=t.id).all()
        total = len(subs)
        done_count = len([s for s in subs if s.done == 1])
        percent = int((done_count / total) * 100) if total else 0
        
        # Süre
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

    return render_template("index.html", tasks=data)

# Ekle
@app.route("/add", methods=["POST"])
def add():
    new_task = Task(
        user_id=session["user"],
        task=request.form["task"],
        category=request.form["category"],
        deadline=request.form["deadline"]
    )
    db.session.add(new_task)
    db.session.commit()
    return redirect("/")

# Düzenle
@app.route("/edit/<int:id>", methods=["POST"])
def edit(id):
    t = Task.query.get_or_404(id)
    t.task = request.form["task"]
    t.category = request.form["category"]
    t.deadline = request.form["deadline"]
    db.session.commit()
    return redirect("/")

# Altgörev
@app.route("/add_sub/<int:id>", methods=["POST"])
def add_sub(id):
    db.session.add(Subtask(task_id=id, text=request.form["text"]))
    db.session.commit()
    return redirect("/")

# Durum
@app.route("/api/done/<int:id>", methods=["POST"])
def api_done(id):
    t = Task.query.get_or_404(id)
    t.done = 1 - t.done
    db.session.commit()
    return jsonify({"status": "success", "is_done": t.done})

# Sil
@app.route("/api/delete/<int:id>", methods=["POST"])
def api_delete(id):
    Subtask.query.filter_by(task_id=id).delete()
    Task.query.filter_by(id=id).delete()
    db.session.commit()
    return jsonify({"status": "success"})

# Altdurum
@app.route("/api/toggle/<int:id>", methods=["POST"])
def api_toggle(id):
    sub = Subtask.query.get_or_404(id)
    sub.done = 1 - sub.done
    db.session.commit()
    
    subs = Subtask.query.filter_by(task_id=sub.task_id).all()
    total = len(subs)
    done_count = len([s for s in subs if s.done == 1])
    percent = int((done_count / total) * 100) if total else 0
        
    return jsonify({"status": "success", "is_done": sub.done, "percent": percent})

# Giriş
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(username=request.form["u"]).first()
        if user and check_password_hash(user.password, request.form["p"]):
            session["user"] = user.id
            return redirect("/")
        flash("Hatalı!")
    return render_template("login.html")

# Kayıt
@app.route("/register", methods=["GET", "POST"])
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

# Çıkış
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# Başlat
if __name__ == "__main__":
    app.run(debug=True)