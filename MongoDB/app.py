from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId

client = MongoClient("mongodb://127.0.0.1:27017")
db = client.project
todos = db.todo

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        todos.insert({"content": task_content, "date_created": datetime.now()})
        return redirect('/')
    else:
        list1 = todos.find()
        return render_template('index.html', tasks=list1)


@app.route('/delete/<task_id>')
def delete(task_id):
    todos.delete_one({"_id": ObjectId(task_id)})
    return redirect('/')


@app.route('/update/<task_id>', methods=['GET', 'POST'])
def update(task_id):
    if request.method == 'POST':
        content = request.form['content']
        todos.update_one({"_id": ObjectId(task_id)}, {"$set": {"content": content}})
        return redirect('/')
    else:
        task1 = todos.find({"_id": ObjectId(task_id)})
        return render_template('update.html', tasks=task1)


if __name__ == "__main__":
    app.run(debug=True)
