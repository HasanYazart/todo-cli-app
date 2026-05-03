import sys
import sqlite3

DB_NAME = "database.db"
# Terminal komutları session bilmediği için varsayılan olarak ID'si 1 olan kullanıcıya ekler.
USER_ID = 1  

def execute_query(query, params=(), fetch=False):
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute(query, params)
        if fetch:
            return cur.fetchall()
        conn.commit()

def add_task(task_text):
    # Kategori ve deadline terminalden alınmadığı için boş bırakıyoruz
    execute_query("INSERT INTO tasks (user_id, task, category, deadline, done) VALUES (?, ?, '', '', 0)", (USER_ID, task_text))
    print(f"Görev eklendi: {task_text}")

def list_tasks(filter_type=None):
    tasks = execute_query("SELECT id, task, done FROM tasks WHERE user_id=?", (USER_ID,), fetch=True)
    
    if not tasks:
        print("Hiç görev yok")
        return

    for task in tasks:
        task_id, text, done = task
        
        if filter_type:
            filter_type = filter_type.lower().strip()

        if filter_type == "done" and not done:
            continue
        if filter_type == "todo" and done:
            continue

        status = "✔️" if done else "❌"
        print(f"{task_id}. [{status}] {text}")

def mark_done(task_id):
    execute_query("UPDATE tasks SET done=1 WHERE id=? AND user_id=?", (task_id, USER_ID))
    print(f"{task_id} ID'li görev tamamlandı.")

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