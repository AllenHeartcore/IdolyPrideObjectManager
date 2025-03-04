import GkmasObjectManager as gom

from flask import Flask, render_template, request, jsonify


app = Flask(__name__)
m = None


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/api/manifest")
def get_manifest():
    global m
    if m is None:
        m = gom.fetch()
    return jsonify(m._get_canon_repr())


if __name__ == "__main__":
    app.run(debug=True, port=5001)
