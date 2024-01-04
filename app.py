from flask import Flask, request, jsonify
from datetime import datetime
from nats_sdk.nats import NatsJetstream
app = Flask(__name__)

@app.route("/trendingdataredis", methods=["GET"])
def trendingdataredis():
    try:
        nats_obj = NatsJetstream()
        nats_obj.connect()
        return (
            jsonify(
                {"status": "success", "data": "data", "timestamp": datetime.now()}
            ),
            200,
        )
    except Exception as e:
        
        error = {"code": 500, "message": str(e)}
        return (
            jsonify({"status": "failed", "data": error, "timestamp": datetime.now()}),
            200,
        )

if __name__ == "__main__":
    app.run()