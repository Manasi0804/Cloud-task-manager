# ✅ Cloud-Powered Task Manager Web App

A modern task manager built with **Flask** and backed by **IBM Cloudant NoSQL Database**, supporting multiple users, intelligent task features, and a clean interface for managing daily to-dos.

---

## 🚀 Features

- **User Registration & Login** – Multi-user support with secure session-based authentication.
- **CRUD Task Operations** – Add, view, update, delete, and toggle task completion.
- **Priority Tagging** – Tag tasks as `High`, `Medium`, or `Low` priority.
- **Due Date Indicators** – Visual cues for `Due Soon` and `Overdue` tasks.
- **Task Categories** – Categorize tasks as `Work`, `Personal`, or `Other`.
- **Weekly Task Summary** – View stats for tasks completed vs pending in the past 7 days.
- **Smart Suggestions** – Auto-prioritize or auto-categorize tasks based on keywords.
- **User Profiles** – Each user sees only their own tasks.
- **Email Digest** *(Coming Soon)* – Optional email summary of tasks.
- **Responsive Design** – Styled using Bootstrap 5.

---

## 💻 Tech Stack

- **Frontend**: HTML, CSS (Bootstrap 5), Jinja2 Templates  
- **Backend**: Flask (Python)
- **Database**: IBM Cloudant NoSQL (2 DBs – `users` and `tasks`)
- **Auth**: Flask Sessions
- **Hosting**: Run locally or deploy to IBM Cloud / Render / Heroku

---

## ⚙️ Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/cloud-task-manager.git
   cd cloud-task-manager
