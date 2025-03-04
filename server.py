import GkmasObjectManager as gom

from flask import Flask, render_template, request, jsonify


app = Flask(__name__)
m = None


def get_manifest():
    global m
    if m is None:
        m = gom.fetch()
    return m


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/api/manifest")
def api_manifest():
    return jsonify(get_manifest()._get_canon_repr())


@app.route("/view/assetbundle/<id>")
def view_assetbundle(id):
    obj = get_manifest().assetbundles[int(id)]
    info = obj._get_canon_repr()
    info["id"] = f"AB{info["id"]:05d}"
    return render_template(
        "view.html",
        info=info,
        embed_url=obj._get_embed_url(),
    )


@app.route("/view/resource/<id>")
def view_resource(id):
    obj = get_manifest().resources[int(id)]
    info = obj._get_canon_repr()
    info["id"] = f"RS{info["id"]:05d}"
    return render_template(
        "view.html",
        info=info,
        embed_url=obj._get_embed_url(),
    )


if __name__ == "__main__":
    app.run(debug=True, port=5001)
