# app.py
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models.todo import Todo

@app.route('/')
def index():
    tasks = Todo.query.order_by(Todo.created_at.desc()).all()
    return render_template('tasks.html', tasks=tasks)

@app.route('/add_task', methods=['POST'])
def add_task():
    title = request.form.get('title')
    description = request.form.get('description')
    if title:
        task = Todo(title=title, description=description)
        db.session.add(task)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/complete_task/<int:id>')
def complete_task(id):
    task = Todo.query.get_or_404(id)
    task.completed = not task.completed
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete_task/<int:id>')
def delete_task(id):
    task = Todo.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)