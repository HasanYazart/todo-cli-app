from flask import Flask, render_template, request, redirect
import json
import os

app = Flask(__name__)

FILE_NAME = "tasks.json"

def load_tasks():
    if not os.path.exists(FILE_NAME):
        return []
    with open(FILE_NAME, "r", encoding="utf-8") as f:
        return json.load(f)

def save_tasks(tasks):
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)

@app.route("/")
def index():
    tasks = load_tasks()
    return render_template("index.html", tasks=tasks)

@app.route("/add", methods=["POST"])
def add():
    task_text = request.form.get("task")
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
    return redirect("/")

@app.route("/done/<int:task_id>")
def done(task_id):
    tasks = load_tasks()

    for task in tasks:
        if task["id"] == task_id:
            task["done"] = True

    save_tasks(tasks)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)