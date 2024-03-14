from flask import Flask, request, jsonify
from datetime import datetime
from nats_sdk.nats import RuleEvents
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

app = Flask(__name__)

@app.route("/trendingdataredis", methods=["GET"])
def trendingdataredis():
    try:
        # nats_obj = RuleEvents()
        # await nats_obj.publish_rule_event(
        #     subject=RuleEvents.rule_create_subject,
        #     event_data={
        #         "rule_name": "dummy rule",
        #         "name": "vishw"
        #     },
        # )
        scheduler = BackgroundScheduler()
        scheduler.start()

        def send_email(start_date, time):
            print("hello world", start_date, time)
            print("@@@@@@###", scheduler.get_jobs())

        def test(start_date, time):
            # scheduled_time = datetime.combine(start_date, time)
            scheduled_time = datetime.strptime(f"{start_date} {time}", "%Y-%m-%d %H:%M:%S")
            scheduler.add_job(
                send_email,
                "date",
                run_date=scheduled_time,
                args=[start_date, time],
            )
            print("@@@@@@", scheduler.get_jobs())

        for i in [
            {"start_date": "2024-03-11", "time": "13:57:00"},
            {"start_date": "2024-03-11", "time": "13:58:00"},
            {"start_date": "2024-03-11", "time": "13:59:00"},
        ]:
            test(start_date=i["start_date"], time=i["time"])
            print("looopppppp")
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
    # from apscheduler.schedulers.background import BackgroundScheduler
    # from datetime import datetime

    # scheduler = BackgroundScheduler()
    # scheduler.start()

    # def send_email(start_date, time):
    #     print("hello world", start_date, time)
    #     print("@@@@@@###", scheduler.get_jobs())

    # def test(start_date, time):
    #     # scheduled_time = datetime.combine(start_date, time)
    #     scheduled_time = datetime.strptime(f"{start_date} {time}", "%Y-%m-%d %H:%M:%S")
    #     scheduler.add_job(
    #         send_email,
    #         "date",
    #         run_date=scheduled_time,
    #         args=[start_date, time],
    #     )
    #     print("@@@@@@", scheduler.get_jobs())

    # for i in [
    #     {"start_date": "2024-03-11", "time": "13:48:00"},
    #     {"start_date": "2024-03-11", "time": "13:49:00"},
    #     {"start_date": "2024-03-11", "time": "13:50:00"},
    # ]:
    #     test(start_date=i["start_date"], time=i["time"])
    #     print("looopppppp")
    app.run()