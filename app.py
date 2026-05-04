from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)
DB = "tasks.db"

def init_db():
    conn = sqlite3.connect(DB)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            done INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

init_db()

def get_db():
    return sqlite3.connect(DB)

@app.route("/")
def index():
    conn = get_db()
    tasks = conn.execute("SELECT * FROM tasks").fetchall()
    conn.close()
    return render_template("index.html", tasks=tasks)

@app.route("/add", methods=["POST"])
def add():
    content = request.form["content"]
    conn = get_db()
    conn.execute("INSERT INTO tasks (content) VALUES (?)", (content,))
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/delete/<int:id>")
def delete(id):
    conn = get_db()
    conn.execute("DELETE FROM tasks WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/toggle/<int:id>")
def toggle(id):
    conn = get_db()
    task = conn.execute("SELECT done FROM tasks WHERE id=?", (id,)).fetchone()
    new = 0 if task[0] == 1 else 1
    conn.execute("UPDATE tasks SET done=? WHERE id=?", (new, id))
    conn.commit()
    conn.close()
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)