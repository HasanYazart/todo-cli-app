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
    tasks.append({"task": task_text})
    save_tasks(tasks)
    print("Görev eklendi:", task_text)

# ---- MAIN ----
args = sys.argv

if len(args) < 2:
    print("Komut gir (add / list)")
    sys.exit()

command = args[1]

if command == "add":
    if len(args) < 3:
        print("Görev yazman lazım")
    else:
        task_text = args[2]
        add_task(task_text)