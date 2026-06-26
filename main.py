import sys
from app import app
from models import db, Task

# Terminal komutları session bilmediği için varsayılan olarak ID'si 1 olan kullanıcıya ekler.
USER_ID = 1  

def add_task(task_text):
    with app.app_context():
        new_task = Task(user_id=USER_ID, task=task_text, category="", deadline="", priority="Low", position=0, done=0)
        db.session.add(new_task)
        db.session.commit()
        print(f"Görev eklendi: {task_text}")

def list_tasks(filter_type=None):
    with app.app_context():
        tasks = Task.query.filter_by(user_id=USER_ID).order_by(Task.position.asc(), Task.id.asc()).all()
        if not tasks:
            print("Hiç görev yok")
            return
            
        for task in tasks:
            if filter_type:
                filter_type = filter_type.lower().strip()
                if filter_type == "done" and not task.done:
                    continue
                if filter_type == "todo" and task.done:
                    continue

            status = "✔️" if task.done else "❌"
            print(f"{task.id}. [{status}] {task.task}")

def mark_done(task_id):
    with app.app_context():
        t = Task.query.filter_by(id=task_id, user_id=USER_ID).first()
        if t:
            t.done = 1
            db.session.commit()
            print(f"{task_id} ID'li görev tamamlandı.")
        else:
            print("Görev bulunamadı.")

# ---- MAIN ----
if __name__ == "__main__":
    args = sys.argv

    if len(args) < 2:
        print("Komut gir (add / list / done)")
        sys.exit()

    command = args[1]

    if command == "add":
        if len(args) < 3:
            print("Görev yazman lazım")
        else:
            add_task(args[2])

    elif command == "list":
        if len(args) == 3:
            list_tasks(args[2])  # done / todo
        else:
            list_tasks()

    elif command == "done":
        if len(args) < 3:
            print("ID girmen lazım")
        else:
            mark_done(int(args[2]))