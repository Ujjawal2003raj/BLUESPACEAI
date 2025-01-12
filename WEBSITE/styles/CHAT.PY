# Open Source AI Business Assistant
# This script demonstrates the basic structure of an AI business assistant with task automation and chatbot capabilities.

from flask import Flask, request, jsonify
from transformers import pipeline
import schedule
import time

app = Flask(__name__)

# Load conversational AI model
chatbot_pipeline = pipeline("conversational", model="microsoft/DialoGPT-medium")

# In-memory task list
tasks = []

# Route: Chatbot functionality
@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message', '')
    response = chatbot_pipeline(user_input)
    return jsonify({'response': response[0]['generated_text']})

# Route: Add a new task
@app.route('/add_task', methods=['POST'])
def add_task():
    task = request.json.get('task', '')
    if task:
        tasks.append(task)
        return jsonify({'message': 'Task added successfully!', 'tasks': tasks})
    return jsonify({'error': 'Task cannot be empty.'}), 400

# Route: Get all tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

# Task Automation Example: Send a reminder
@app.route('/reminder', methods=['POST'])
def set_reminder():
    task = request.json.get('task', '')
    time_interval = request.json.get('time', 1)  # Default to 1 minute

    def reminder():
        print(f"Reminder: {task}")

    schedule.every(time_interval).minutes.do(reminder)
    return jsonify({'message': f'Reminder set for every {time_interval} minute(s).', 'task': task})

# Run scheduled tasks
@app.before_first_request
def run_scheduler():
    def run_continuously():
        while True:
            schedule.run_pending()
            time.sleep(1)

    import threading
    threading.Thread(target=run_continuously, daemon=True).start()

if __name__ == '__main__':
    app.run(debug=True)
