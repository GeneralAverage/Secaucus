from flask import Flask, render_template, redirect, url_for, request, send_from_directory
from werkzeug.utils import secure_filename
import os
from datetime import datetime

app = Flask(__name__, template_folder='templates')
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

database = {'GeneralAverage': 'ml623148'}
history = []
currentuser = None

@app.route("/", methods=['GET', 'POST'])
def mainpage():
    return render_template('mainpage.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    error = False
    if request.method == 'POST':
        username = str(request.form['username'])
        password = str(request.form['password'])
        if username not in database or password != database[username]:
            raise NotImplementedError('bruh')
        else:
            global currentuser
            currentuser = 'GeneralAverage'
            return render_template('mainpage.html')
    return render_template('login.html')
@app.route("/signup", methods=['GET', 'POST'])
def signup():
    error = False
    if request.method == 'POST':
        username = str(request.form['username'])
        password = str(request.form['password'])
        if username in database or len(password) < 1:
            raise TypeError("Username in Use or invalid password.")
        else:
            database.update({username:password})
            global currentuser
            currentuser = username
            return render_template('mainpage.html')
    return render_template('signup.html')
@app.route("/submitmsg", methods=['GET', 'POST'])
def submitmsg():
    global history
    if request.method == 'POST':
        try:
            msg = str(request.form['msg'])
            title = str(request.form['title'])
            file = request.files['file']
            if currentuser:
                username = currentuser
            else:
                raise PermissionError
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            if file:
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                history.append({'username': username, 'msg': msg, 'title': title, 'timestamp': timestamp, 'filename': filename, 'comments': []})
            else:
                history.append({'username': username, 'msg': msg, 'title': title, 'timestamp': timestamp, 'filename': None, 'comments': []})
            return redirect(url_for('viewposts'))
        except PermissionError:
            raise PermissionError('Insufficient Permissions!')
    else:
        return render_template('submitmsg.html')

@app.route('/uploads/<filename>', methods=['GET', 'POST'])
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route("/viewposts", methods=['GET', 'POST'])
def viewposts():
    return render_template('viewposts.html', history=history)

@app.route("/post/<int:post_id>", methods=['GET', 'POST'])
def viewpost(post_id):
    post = history[post_id]
    if request.method == 'POST':
        comment_text = str(request.form['comment'])
        commenter_name = currentuser
        post['comments'].append({'username': commenter_name, 'comment': comment_text, 'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
    return render_template('viewpost.html', post=post, post_id=post_id)


if __name__ == '__main__':
    app.run(debug=True, port=8081)
