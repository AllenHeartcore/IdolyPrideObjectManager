import GkmasObjectManager as gom

from flask import Flask, render_template, request, jsonify


app = Flask(__name__)
m = None


def _get_manifest():
    global m
    if m is None:
        m = gom.fetch()
    return m


def _abid2name(id):
    return _get_manifest().assetbundles[int(id)].name


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/api/manifest")
def api_manifest():
    return jsonify(_get_manifest()._get_canon_repr())


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
    info["embed_url"] = obj._get_embed_url()
    return jsonify(info)


@app.route("/api/resource/<id>")
def api_resource(id):
    obj = _get_manifest().resources[int(id)]
    info = obj._get_canon_repr()
    info["id"] = f"Resource #{info["id"]}"
    info["embed_url"] = obj._get_embed_url()
    return jsonify(info)


@app.route("/view/assetbundle/<id>")
def view_assetbundle(id):
    return render_template("view.html", id=id, type="assetbundle")
    # Used to query obj here and pass obj._get_canon_repr() and obj._get_embed_url()
    # directly to the template, but if user starts at viewpage instead of homepage,
    # manifest + object fetch (both handled by backend) will create a serious delay,
    # during which time we must display a loading spinner. Thus these logic are now
    # packed in an API call, and view.js handles dependency list rendering altogether.


@app.route("/view/resource/<id>")
def view_resource(id):
    return render_template("view.html", id=id, type="resource")


if __name__ == "__main__":
    app.run(debug=True, port=5001)
