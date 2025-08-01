from flask import Flask, request, render_template, redirect, session
from cloudant import Cloudant
from dotenv import load_dotenv
from datetime import datetime, timedelta
import os

load_dotenv()
app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Load environment variables
cloudant_username = os.getenv("CLOUDANT_USERNAME")
cloudant_apikey = os.getenv("CLOUDANT_APIKEY")
cloudant_url = os.getenv("CLOUDANT_URL")
task_dbname = os.getenv("TASKS_DB")
user_dbname = os.getenv("USERS_DB")

# Connect to Cloudant
client = Cloudant.iam(cloudant_username, cloudant_apikey, url=cloudant_url, connect=True)
task_db = client.create_database(task_dbname, throw_on_exists=False)
user_db = client.create_database(user_dbname, throw_on_exists=False)

# Custom Jinja filter to convert date string to datetime object
@app.template_filter('todatetime')
def to_datetime_filter(value):
    try:
        return datetime.strptime(value, "%Y-%m-%d")
    except Exception:
        return value

@app.before_request
def require_login():
    allowed_routes = ['login', 'register']
    if request.endpoint not in allowed_routes and 'logged_in' not in session:
        return redirect('/login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        new_user = request.form['username']
        new_pass = request.form['password']
        if any(doc for doc in user_db if doc.get('username') == new_user):
            return render_template("register.html", error="Username already exists.")
        user_db.create_document({'username': new_user, 'password': new_pass})
        return redirect('/login')
    return render_template("register.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        input_user = request.form['username']
        input_pass = request.form['password']
        user = next((doc for doc in user_db if doc.get('username') == input_user and doc.get('password') == input_pass), None)
        if user:
            session['logged_in'] = True
            session['username'] = input_user
            return redirect('/')
        return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/')
def home():
    username = session['username']
    tasks = [doc for doc in task_db if doc.get('username') == username]
    return render_template('index.html', tasks=tasks, now=datetime.utcnow())

@app.route('/add', methods=['POST'])
def add_task():
    task = request.form['task']
    priority = request.form['priority']
    category = request.form['category']
    due_date = request.form['due_date']

    # Smart suggestion override
    if 'urgent' in task.lower() or 'asap' in task.lower():
        priority = 'High'
    elif 'call' in task.lower() or 'remind' in task.lower():
        category = 'Personal'

    task_db.create_document({
        'type': 'task',
        'task': task,
        'completed': False,
        'username': session['username'],
        'priority': priority,
        'category': category,
        'due_date': due_date
    })
    return redirect('/')

@app.route('/update/<task_id>', methods=['POST'])
def update_task(task_id):
    task = task_db[task_id]
    task['task'] = request.form['updated_task']
    task.save()
    return redirect('/')

@app.route('/delete/<task_id>', methods=['POST'])
def delete_task(task_id):
    task_db[task_id].delete()
    return redirect('/')

@app.route('/toggle/<task_id>', methods=['POST'])
def toggle_task(task_id):
    task = task_db[task_id]
    task['completed'] = not task.get('completed', False)
    task.save()
    return redirect('/')

@app.route('/task/<task_id>')
def view_task(task_id):
    task = task_db.get(task_id)
    if task:
        return render_template('task_detail.html', task=task)
    return "Task not found", 404

@app.route('/summary')
def summary():
    username = session['username']
    tasks = [doc for doc in task_db if doc.get('username') == username]

    this_week = datetime.utcnow() - timedelta(days=7)
    recent_tasks = [
        t for t in tasks
        if t.get('due_date') and datetime.strptime(t['due_date'], "%Y-%m-%d") >= this_week
    ]

    done = sum(1 for t in recent_tasks if t.get('completed'))
    pending = len(recent_tasks) - done

    return render_template('summary.html', done=done, pending=pending, total=len(recent_tasks))

if __name__ == '__main__':
    app.run(debug=True)
