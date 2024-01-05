from flask import Flask, request, jsonify
from datetime import datetime
from nats_sdk.nats import RuleEvents
app = Flask(__name__)

@app.route("/trendingdataredis", methods=["GET"])
async def trendingdataredis():
    try:
        nats_obj = RuleEvents()
        await nats_obj.publish_rule_event(
            subject=RuleEvents.rule_create_subject,
            event_data={
                "rule_name": "dummy rule",
                "name": "vishw"
            },
        )
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