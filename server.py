import GkmasObjectManager as gom

from flask import Flask, render_template, request, jsonify


app = Flask(__name__)
manifest = None


@app.route("/")
def welcome():
    return render_template("layout.html")


if __name__ == "__main__":
    app.run(debug=True, port=5001)
