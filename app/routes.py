from flask import render_template, request, redirect, url_for
from app import app
import json

with open("app/tasks.json", "r") as file:
    tasks = json.load(file)

def save_tasks():
    with open("app/tasks.json", "w") as file:
        json.dump(tasks, file, indent=4)

@app.route('/')
@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html", tasks=tasks)

@app.route("/add-task", methods=["GET", "POST"])
def add_task():
    if request.method == "POST":
        task_name = request.form["task_name"].strip()
        class_name = request.form["class_name"].strip()
        due_date = request.form["due_date"]

        if task_name and class_name:
            tasks.append({
                "name": task_name,
                "class": class_name,
                "date": due_date,
                "completed": False
            })
            save_tasks()

        return redirect(url_for("dashboard"))

    return render_template("add_task.html")

@app.route("/delete-task/<int:index>")
def delete_task(index):
    tasks.pop(index)
    save_tasks()
    return redirect(url_for("dashboard"))

@app.route("/complete-task/<int:index>", methods=["POST"])
def complete_task(index):
    tasks[index]["completed"] = True
    return redirect(url_for("dashboard"))
