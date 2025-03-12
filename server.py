import GkmasObjectManager as gom

from flask import Flask, render_template, request, jsonify, Response


# Bookkeeping


app = Flask(__name__)
m = None


def _get_manifest():
    global m
    if m is None:
        m = gom.load("manifest.json")
    return m


# API endpoints


@app.route("/api/manifest")
def api_manifest():
    return jsonify(_get_manifest()._get_canon_repr())


@app.route("/api/search")
def api_search():
    query = request.args.get("query", "")
    return jsonify(
        [
            {
                "id": obj.id,
                "name": obj.name,
                "type": type(obj).__name__[5:],  # valid names start with "Gkmas"
            }
            for obj in _get_manifest().search(
                "".join(f"(?=.*{word})" for word in query.split())
                # use lookahead to match all words in any order
            )
        ]
    )


@app.route("/api/<id>/caption")
def api_caption(id):
    return _get_manifest().resources[int(id)].get_caption()


# Frontend routes


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/search")
def search():
    query = request.args.get("query", "")
    return render_template("search.html", query=query)


@app.route("/view/<id>")
def view(id):

    try:
        obj = _get_manifest().resources[int(id)]
    except KeyError:
        return render_template("404.html"), 404

    info = obj._get_canon_repr()
    return render_template("view.html", info=info, type="Resource")


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True, port=5001)
