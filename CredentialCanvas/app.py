from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory, jsonify
import os, json

app = Flask(__name__)
app.secret_key = "supersecret"

user1 = "meow"
password1 = "catfood"

user2 = "verstappen"
password2 = "gridmaster"

BLOG_FILE = "blogs.json"

def load_blogs():
    if os.path.exists(BLOG_FILE):
        with open(BLOG_FILE, "r") as f:
            return json.load(f)
    return []

def save_blogs(blogs):
    with open(BLOG_FILE, "w") as f:
        json.dump(blogs, f, indent=4)

def load_users():
    if os.path.exists("users.json"):
        with open("users.json", "r") as f:
            return json.load(f)
    return {}        

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    if username == user1 and password == password1:
        session['authenticated'] = True
        session['username'] = username.strip()  # store username properly
        return redirect(url_for('flag'))
    
    if username == user2 and password == password2:
        session['authenticated'] = True
        session['username'] = username.strip()  # store username properly
        return redirect(url_for('flag2'))

    else:
        return render_template('index.html', error_message="Invalid credentials")
    
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    users = load_users()
    
    if request.method == 'POST':
        data = request.get_json()
        if not data or 'username' not in data:
            return "Username not provided", 400
        username = data['username']
    else:  # GET request
        # Default to currently logged-in user
        username = session.get('username')
        if not username:
            return redirect(url_for('index'))

    password = users.get(username)
    if not password:
        return "User not found", 404

    return render_template('profile.html', username=username, password=password)

@app.route('/dashboard')
def dashboard():
    if session.get('authenticated'):
        blogs = load_blogs()
        current_user = session.get('username')
        return render_template('dashboard.html', blogs=blogs, current_user=current_user)
    else:
        return redirect(url_for('index'))

@app.route('/myblogs', methods=['GET', 'POST'])
def myblogs():
    if not session.get('authenticated'):
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        author = session.get('username')
        if title and content:
            blogs = load_blogs()
            blogs.insert(0, {"title": title, "content": content, "author": author})  # newest first
            save_blogs(blogs)
        return redirect(url_for('dashboard'))

    return render_template('myblogs.html')

@app.route('/delete_blog/<int:blog_index>', methods=['POST'])
def delete_blog(blog_index):
    if not session.get('authenticated'):
        return redirect(url_for('index'))

    blogs = load_blogs()
    if 0 <= blog_index < len(blogs):
        blog = blogs[blog_index]
        # Only allow deletion if current user is the author
        if blog.get('author') == session.get('username'):
            del blogs[blog_index]
            save_blogs(blogs)
    return redirect(url_for('dashboard'))

@app.route('/flag')
def flag():
    if session.get('authenticated'):
        if session.get('username') != user1:
            return "Not authorized", 403
        return render_template('flag.html', flag="CTFEYDSCI{d15gu153d_c4tf00d_p455}")
    else:
        return redirect(url_for('index'))
    
@app.route('/flag2')
def flag2():
    if session.get('authenticated'):
        if session.get('username') != user2:
            return "Not authorized", 403
        return render_template('flag2.html', flag2="CTFEYDSCI{d15gu153d_r4c3r_p455}")
    else:
        return redirect(url_for('index'))

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('index'))

# Hidden image route (unchanged)
@app.route('/supersecreturl/cat.jpg')
def cat_image():
    return send_from_directory(os.path.join(app.root_path, 'supersecreturl'), 'cat.jpg')

@app.route('/backup')
def backup():
    return render_template('backup.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
