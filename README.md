Secure File Sharing System
A simple way for teams to share files safely

# What This Project Does
Ops Users can upload files (PPTX, DOCX, XLSX only)

Client Users can sign up, verify their email, and download files

Every download link is secure – only approved clients can access files

# Quick Start Guide
1. Install Requirements
(You’ll need these before starting)

Python 3.8+ (Download: python.org)

Git (For code management)

PostgreSQL (Recommended) or SQLite (Simple, no setup needed)

2. Setup the Project
(Follow these steps one by one)

🔹 Step 1: Download the Code
git clone https://github.com/yourusername/secure-file-sharing.git
cd secure-file-sharing

🔹 Step 2: Create a Virtual Environment
(Keeps Python packages organized)
python -m venv venv
Windows: Run venv\Scripts\activate

Mac/Linux: Run source venv/bin/activate

🔹 Step 3: Install Packages
pip install -r requirements.txt

🔹 Step 4: Run Migrations
(Prepares the database)
python manage.py migrate

🔹 Step 5: Create Admin User
(For accessing the admin panel)
python manage.py createsuperuser
Follow prompts to set username/email/password

🔹 Step 6: Run the Server
python manage.py runserver
Open: http://localhost:8000

# Key Features
For Ops Users
✅ Login – Get a secure token
✅ Upload Files – Only PPTX, DOCX, XLSX allowed

For Client Users
✅ Sign Up – Email verification required
✅ Login – After email confirmation
✅ Download Files – Via secure links
✅ List Files – See all uploaded files

# Extra Points 

1. Test Cases

We’ve added tests to check:
✔ User registration & login
✔ File uploads (only allowed formats)
✔ Secure downloads (only for verified clients)

Run tests with:
python manage.py test

2. Deployment Plan (For Going Live)

1. Choose a Host (Pick one)
Railway.app (Easiest) → railway.app

Heroku (Free) → heroku.com

2. Prepare Your Project
Install:
pip install gunicorn whitenoise psycopg2-binary python-dotenv
Create .env file:
DEBUG=False
SECRET_KEY=your-secret-key
Update settings.py (use os.getenv() for secrets).

3. Deploy on Railway (Fastest)
Sign up at Railway.app.

Upload code (drag & drop or GitHub).

Set SECRET_KEY in "Variables" tab.

Run:
railway run python manage.py migrate
railway run python manage.py createsuperuser
Done! Your site is live.

Or Deploy on Heroku
Sign up at Heroku.

Run:
heroku create
git push heroku main
heroku run python manage.py migrate
Done! 

Keep Secure
Never share .env or SECRET_KEY.

Use DEBUG=False in production.

Your app is now live! 

# Admin Panel (For Managing Users & Files)
Access: http://localhost:8000/admin

What You Can Do:

👥 Manage users (Ops & Clients)

📂 View uploaded files

🔗 Monitor download links

