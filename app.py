from flask import Flask, request, jsonify, render_template, redirect
from cloudant import Cloudant
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

# Connect to IBM Cloudant
cloudant_url = os.getenv("CLOUDANT_URL")
cloudant_apikey = os.getenv("CLOUDANT_APIKEY")
cloudant_dbname = os.getenv("CLOUDANT_DB")
cloudant_username = os.getenv("CLOUDANT_USERNAME")

client = Cloudant.iam(cloudant_username, cloudant_apikey, url=cloudant_url, connect=True)
db = client.create_database(cloudant_dbname, throw_on_exists=False)

#Read all tasks
@app.route('/', methods=['GET'])
def home():
    tasks = [doc for doc in db]
    return render_template('index.html', tasks=tasks)

#Create a task
@app.route('/add', methods=['POST'])
def add_task():
    task = request.form['task']
    db.create_document({'task': task})
    return redirect('/')

#Update a task
@app.route('/update/<task_id>', methods=['POST'])
def update_task(task_id):
    task = db[task_id]
    task['task'] = request.form['updated_task']
    task.save()
    return redirect('/')

#Delete a task
@app.route('/delete/<task_id>', methods=['POST'])
def delete_task(task_id):
    db[task_id].delete()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
