from flask import Flask, render_template, url_for, request, redirect
from flask import session as login_session
import pyrebase
import os

app = Flask(  # Create a flask app
    __name__,
    template_folder='templates',  # Name of html file folder
    static_folder='static'  # Name of directory for static files
)

UPLOAD_FOLDER = 'static/images/posts'
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']


config = {
  "apiKey": "AIzaSyDRuLBANJse7Wv4CYr57iw3hdejZ0TV-Jk",
  "authDomain": "lab1cs.firebaseapp.com",
  "projectId": "lab1cs",
  "storageBucket": "lab1cs.appspot.com",
  "messagingSenderId": "61711755948",
  "appId": "1:61711755948:web:1b6fe30606ed0c38158d09",
  "measurementId": "G-E29PZC7JE1",
  "databaseURL": "https://lab1cs-default-rtdb.firebaseio.com"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def upload_file(file):
    if request.method == 'POST':
        if file and allowed_file(file.filename):
            filename = file.filename
            file.save(UPLOAD_FOLDER + '/' + filename)


@app.route('/')  # '/' for the default page
def home():
    posts  = db.child("Posts").get().val()
    return render_template("index.html", posts  = posts)


@app.route('/add_post', methods = ['GET', 'POST'])  # '/' for the default page
def add_post():
    if request.method == 'POST':
        caption = request.form['caption']
        photo = request.files['post_pic']
        upload_file(photo)
        post = {"caption": caption, "photo": photo.filename}
        db.child("Posts").push(post)

        return redirect("/")
        
    return render_template('add_post.html')

# @app.route('/all_posts')
# def all_posts():
#     # post = db.child("Posts").child(login_session["user"]["localId"]).get().val()
#     post = db.child("Posts").get().val()
#     return render_template("all_posts.html", post = post)


if __name__ == "__main__":  # Makes sure this is the main process
    app.run(debug=True)
