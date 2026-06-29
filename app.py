from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def home():
    return jsonify({
        "project": "MiniCrypto Blockchain",
        "status": "running"
    })


@app.route("/test")
def test():
    return jsonify({
        "message": "Flask API working"
    })


if __name__ == "__main__":
    app.run(debug=True)