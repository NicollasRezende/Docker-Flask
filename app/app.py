from flask import Flask, jsonify, request

app = Flask(__name__)

tasks = []

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)

@app.route('/tasks', methods=['POST'])
def add_task():
    task = request.json
    tasks.append(task)
    return jsonify(task), 201

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = next((t for t in tasks if t.get('id') == task_id), None)
    if task is None:
        return jsonify({'error': 'Task not found'}), 404
    updated_task = request.json
    task.update(updated_task)
    return jsonify(task)

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    tasks = [t for t in tasks if t.get('id') != task_id]
    return jsonify({'result': 'Task deleted'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
