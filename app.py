from flask import Flask,render_template
app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/khaoyai')
def khaoyai():
    return render_template("khaoyai.html")

@app.route('/search')
def search():
    return render_template("search.html")

@app.route('/check')
def check():
    return render_template("check.html")



if __name__ == "__main__":
    app.run(debug=True)