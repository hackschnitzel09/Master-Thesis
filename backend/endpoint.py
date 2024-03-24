from flask import Flask, jsonify, request, make_response
from flask_cors import CORS, cross_origin
import json

db= "todos.json"

app = Flask(__name__) 
CORS(app)


def get_task_r():
    #read tasks from json db
    with open(db, 'r') as f:
        tasks= json.load(f)
    f.close
    return tasks

def get_tasks_w(tasks):
    with open(db, 'w') as f:
        json.dump(tasks, f)
    f.close

#GET all
@app.route('/tasks', methods=['GET'])
def get_tasks():    
    return jsonify(get_task_r())

#GET one Task
@app.route('/tasks/<int:id>', methods=['GET'])
def task_by_id(id: int):
    if id >= len(get_task_r()):
        return jsonify({ 'error': 'Task does not exist'}), 404
    return jsonify(get_task_r()[str(id)])
    
#PUT
@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id: int):
    tasks= get_task_r()
    if tasks.get(str(id), None) == None: return {'error': 'Task not found' }, 404
    tasks[str(id)]= json.loads(request.data)
    get_tasks_w(tasks)

    #400

    return jsonify(tasks[str(id)])

next_id= 0
#POST
@app.route('/tasks', methods=['POST'])
def add_task():
    global next_id
    tasks= get_task_r()
    #if no task there
    print(list(tasks.keys()))
    if not list(tasks.keys()): 
        next_id= 0
    else:
        #next_id= 1+int(max(list(tasks.keys())))
        next_id += 1
    # put body at the end of db file (open, update, close)
    tasks[next_id]=(request.get_json())
    get_tasks_w(tasks)
    return jsonify({"message": "Task wurde hinzugefügt"}), 201

#DELETE
@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id: int):
    tasks= get_task_r()
    print(tasks.get(str(id)))
    if tasks.get(str(id), None) == None: return {'error': 'Task not found' }, 404
    task= tasks[str(id)]
    tasks.pop(str(id))
    get_tasks_w(tasks)
    return jsonify(task), 200