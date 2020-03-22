#!flask/bin/python
from flask import Flask, jsonify
from flask import request
from flask import make_response
from flask import abort
import gpio_motor_control as motor_control


app = Flask(__name__)

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
        'done': False
    }
]

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/commands', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

@app.route('/commands', methods=['POST'])
def create_task():
    if not request.json or not 'command' in request.json:
        abort(400)
    command = request.json['command']
    if "speed" in request.json:
        speed = int(request.json["speed"])
    else:
        speed = 0
    if command == "stop":
        motor_control.speed(speed)
        motor_control.stop() 
        
    elif command == "forward":
        motor_control.speed(speed)
        motor_control.forward()
        
    elif command == "reverse":
        motor_control.speed(speed)
        motor_control.reverse()
        
    else:
        motor_control.stop()
        motor_control.speed(speed)
    return jsonify({'task': command}), 201

if __name__ == '__main__':
    app.run(debug=True, host= '0.0.0.0')