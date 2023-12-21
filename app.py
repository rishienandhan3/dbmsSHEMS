from flask import Flask, redirect, url_for, render_template

# create a Flask App instance:
app = Flask(__name__)


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/<name>/')
def user(name):
    return f"<h3> Hello {name}! </h3>"


@app.route('/admin/')
def admin():
    return redirect(url_for('user', name='Admin!'))


@app.route('/printname/<name>/')
def printname(name):
    return render_template("print.html", content=name)


if __name__ == '__main__':
    app.run(debug=True)
