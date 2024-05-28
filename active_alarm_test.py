import os
import asyncio
import nats
from nats.errors import TimeoutError
import random
from datetime import datetime, timezone
import time
import json
import pytz
import time
import uuid

servers = os.environ.get("NATS_URL", "nats://192.168.4.50:4222").split(",")


async def main():
    nc = await nats.connect(servers=servers)
    date = datetime.now(pytz.utc)
    timestamp = time.time()

    severity_index = round(random.uniform(0, 3))
    status_index = round(random.uniform(0, 1))
    asste_tag_index = round(random.uniform(0, 20))

    severity = ["INFORMATION", "MAJOR", "MINOR", "CRITICAL"]
    status = ["ACTIVE", "RESOLVED"]

    asset_tags = [
        "AI-JNCCC-SERV-005",
        "AI-SAIFT5-SWA-004",
        "AI-SAIFP6-CREX-001",
        "AI-SAIFP6-SWA-002",
        "AI-SAIFT5-SWA-001",
        "AI-JNCCC-SERV-004",
        "AI-JNCCC-SWA-001",
        "AI-SAIFP6-SWA-001",
        "AI-SAIFP6-FCAM-001",
        "AI-SAIFT5-SWA-002",
        "AI-JNCCC-PCAM-002",
        "AI-SAIFT5-SERV-001",
        "AI-SAIFT5-SWA-003",
        "AI-SAIFP6-FCAM-002",
        "AI-SAIFP6-SERV-001",
        "AI-JNCCC-UWS-001",
        "AI-SAIFP6-FCAM-005",
        "AI-SAIFP6-ACP-001",
        "AI-JNCCC-PCAM-001",
        "AI-JNCCC-SERV-002",
        "AI-SAIFP6-CREN-001",
    ]

    source_objs = ["5/0", "5/1", "5/2", "5/3"]

    data = {
        "data": {
            "time": timestamp,
            "timestamp": str(date),
            "time_ns": timestamp,
            "severity_n": severity[severity_index],
            "severity": severity_index,
            "status_n": status[status_index],
            "description": "TEST ALARM 1",
            "source_data": None,
            "source_alarm_id": str(uuid.uuid4()),
            "trigger_id": str(uuid.uuid4()),
            "source_object_id": source_objs[severity_index],
            "id": str(uuid.uuid4()),
            "asset_tag": asset_tags[asste_tag_index],
            "asset_id": str(uuid.uuid4()),
            "status": status_index,
        },
        "timestamp": str(date),
        "event": "NEW_ALARM",
    }

    event_data = json.dumps(data)
    await nc.publish("new_active_alarm.*", event_data.encode())
    await nc.drain()


if __name__ == "__main__":
    while True:
        asyncio.run(main())
        print("data published")
        time.sleep(5)
