from flask import render_template, request, redirect, url_for
from app import app
import json

with open("app/tasks.json", "r") as file:
    tasks = json.load(file)

with open("app/classes.json", "r") as file:
    classes = json.load(file)

def save_tasks():
    with open("app/tasks.json", "w") as file:
        json.dump(tasks, file, indent=4)

def save_classes():
    with open("app/classes.json", "w") as file:
        json.dump(classes, file, indent=4)

@app.route("/")
@app.route("/dashboard")
def dashboard():
    active_tasks = [task for task in tasks if not task["completed"]]
    return render_template("dashboard.html", tasks=active_tasks, classes=classes)

@app.route("/add-class", methods=["GET", "POST"])
def add_class():
    if request.method == "POST":
        class_name = request.form["class_name"].strip()

        if class_name:
            classes.append({
                "name": class_name,
            })
            save_classes()

        return redirect(url_for("dashboard"))

    return render_template("add_class.html")

@app.route("/add-task", methods=["GET", "POST"])
def add_task():
    if request.method == "POST":
        task_name = request.form["task_name"].strip()
        class_name = request.form["class_name"].strip()
        due_date = request.form["due_date"]

        if task_name:
            tasks.append({
                "name": task_name,
                "class": class_name,
                "date": due_date,
                "completed": False
            })
            save_tasks()

        return redirect(url_for("dashboard"))

    return render_template("add_task.html", classes=classes)

@app.route("/delete-task/<int:index>")
def delete_task(index):
    tasks.pop(index)
    save_tasks()
    return redirect(url_for("dashboard"))

@app.route("/complete-task/<int:index>", methods=["POST"])
def complete_task(index):
    with open("app/tasks.json", "r") as file:
        tasks = json.load(file)

    tasks[index]["completed"] = True

    with open("app/tasks.json", "w") as file:
        json.dump(tasks, file)

    return redirect(url_for("dashboard"))

@app.route("/completed")
def completed():
    with open("app/tasks.json", "r") as file:
        tasks = json.load(file)

    completed_tasks = [task for task in tasks if task.get("completed") == True]

    return render_template("completed.html", tasks=completed_tasks)