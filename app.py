from flask import Flask, render_template, redirect

app = Flask(__name__)

@app.route('/')
def index():
    return "Welcome to my site, please sure to use /YOURNAME to get a nice page with your name.\nAlso, you can do /main in order to access the best SITE ever!!"

@app.route('/<name>')
def getName(name):
    return f"Welcome! {name}, this is the best app you will see."

@app.route('/main')
def showSite():
    return render_template('main.html')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)