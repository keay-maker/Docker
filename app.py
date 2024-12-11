from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:secret@db:5432/postgres'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(100), nullable=False)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        db.session.add(Todo(task=request.form["task"]))
        db.session.commit()
        
        return redirect(url_for("index"))

    todos = Todo.query.all()

    return render_template("index.html", todos=todos)


def init_db():
    db.create_all()

if __name__ == "__main__":
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)