import GkmasObjectManager as gom

from flask import Flask, render_template, request, jsonify
import re


# Bookkeeping


app = Flask(__name__)
m = None


def _get_manifest():
    global m
    if m is None:
        m = gom.fetch()
    return m


def _abid2name(id):
    return _get_manifest().assetbundles[int(id)].name


# API endpoints


@app.route("/api/manifest")
def api_manifest():
    return jsonify(_get_manifest()._get_canon_repr())


@app.route("/api/search/<query>")
def api_search(query):
    return jsonify(
        [
            {
                "id": obj.id,
                "name": obj.name,
                "type": type(obj).__name__[5:],  # valid names start with "Gkmas"
            }
            for obj in _get_manifest().search(
                "".join(f"(?=.*{re.escape(word)})" for word in query.split())
                # use lookahead to match all words in any order
            )
        ]
    )


@app.route("/api/assetbundle/<id>")
def api_assetbundle(id):
    obj = _get_manifest().assetbundles[int(id)]
    info = obj._get_canon_repr()
    info["id"] = f"AssetBundle #{info["id"]}"
    if "dependencies" in info:
        info["dependencies"] = [
            {
                "id": dep,
                "name": _abid2name(dep),
            }
            for dep in info["dependencies"]
        ]
    info["mimetype"] = obj.get_mimetype()
    return jsonify(info)


@app.route("/api/assetbundle/<id>/bytestream")
def api_assetbundle_bytestream(id):
    return _get_manifest().assetbundles[int(id)].get_bytestream()


@app.route("/api/assetbundle/<id>/caption")
def api_assetbundle_caption(id):
    return _get_manifest().assetbundles[int(id)].get_caption()


@app.route("/api/resource/<id>")
def api_resource(id):
    obj = _get_manifest().resources[int(id)]
    info = obj._get_canon_repr()
    info["id"] = f"Resource #{info["id"]}"
    info["mimetype"] = obj.get_mimetype()
    return jsonify(info)


@app.route("/api/resource/<id>/bytestream")
def api_resource_bytestream(id):
    return _get_manifest().resources[int(id)].get_bytestream()


@app.route("/api/resource/<id>/caption")
def api_resource_caption(id):
    return _get_manifest().resources[int(id)].get_caption()


# Frontend routes


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/search/<query>")
def search(query):
    return render_template("search.html", query=query)


@app.route("/view/assetbundle/<id>")
def view_assetbundle(id):
    return render_template("view.html", id=id, type="AssetBundle")
    # Used to query obj here and pass obj._get_canon_repr(), bytes, and mimetype
    # directly to the template, but if user starts at viewpage instead of homepage,
    # manifest + object fetch (both handled by backend) will create a serious delay,
    # during which time we must display a loading spinner. Thus these logic are now
    # packed in an API call, and view.js handles dependency list rendering altogether.


@app.route("/view/resource/<id>")
def view_resource(id):
    return render_template("view.html", id=id, type="Resource")


if __name__ == "__main__":
    app.run(debug=True, port=5001)
