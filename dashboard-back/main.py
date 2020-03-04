from flask import Flask, render_template


app = Flask(__name__,
            static_folder="../dashboard-front/dist/",
            template_folder="../dashboard-front/dist")


@app.route('/')
def index():
    return render_template("index.html")