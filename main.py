import sys
import json
import os

FILE_NAME = "tasks.json"

def load_tasks():
    if not os.path.exists(FILE_NAME):
        return []
    with open(FILE_NAME, "r", encoding="utf-8") as f:
        return json.load(f)

def save_tasks(tasks):
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)

def add_task(task_text):
    tasks = load_tasks()
    
    new_id = 1
    if tasks:
        new_id = max(task["id"] for task in tasks) + 1

    tasks.append({
        "id": new_id,
        "task": task_text,
        "done": False
    })

    save_tasks(tasks)
    print(f"Görev eklendi (ID: {new_id}): {task_text}")

def list_tasks(filter_type=None):
    tasks = load_tasks()
    
    if not tasks:
        print("Hiç görev yok")
        return

    for task in tasks:
        # filtreyi normalize et
        if filter_type:
            filter_type = filter_type.lower().strip()

        if filter_type == "done" and task["done"] is False:
            continue

        if filter_type == "todo" and task["done"] is True:
            continue

        status = "✔️" if task["done"] else "❌"
        print(f"{task['id']}. [{status}] {task['task']}")

def mark_done(task_id):
    tasks = load_tasks()
    
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = True
            save_tasks(tasks)
            print(f"{task_id} tamamlandı")
            return

    print("Böyle bir ID yok")

# ---- MAIN ----
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