import os
import asyncio
import nats
from nats.errors import TimeoutError
import random
from datetime import datetime, timezone
import time
import json 
servers = os.environ.get("NATS_URL", "nats://192.168.3.171:4222").split(",")


async def main():

    nc = await nats.connect(servers=servers)
    random_value = random.uniform(0, 0.6)
    data = {
            "data": {
                "fpi": str(random_value),
                "time": str(datetime.now(timezone.utc))
            },
            "event": "fpi",
            "timestamp": str(datetime.now(timezone.utc))
        }
    event_data = json.dumps(data)
    await nc.publish("fpi.joe", event_data.encode())

    if random_value > 0.5:
        data = {
            "data": {
                "type": "FPI",
                "id": "",
                "message": "{1} High Current reading is {2}. Immediate action required.",
                "message_values": ["FPI Alert:", str(round(random_value, 2))],
                "extra": {
                "fpi": random_value
                }
            },
            "event": 'Notification',
            "timestamp": str(datetime.now(timezone.utc)),
        }
        event_data = json.dumps(data)
        await nc.publish("notification.joe", event_data.encode())
    # sub = await nc.subscribe("greet.*")

    # try:
    #     msg = await sub.next_msg(timeout=0.1)
    # except TimeoutError:
    #     pass
    
    # while True:
    #     random_value = random.uniform(0.4, 0.5)
    #     # data = {
    #     #     "data": {
    #     #         "fpi": str(random_value),
    #     #         "time": str(datetime.now(timezone.utc))
    #     #     },
    #     #     "event": "fpi",
    #     #     "timestamp": str(datetime.now(timezone.utc))
    #     # }
    #     await nc.publish("fpi.v", b"data")
    #     # await nats_obj.publish_data(subject="fpi.*", event_data=data)

    #     # random_valueav = random.uniform(0.95, 1)
    #     # data_av = {
    #     #     "data": {
    #     #         "avaibility": str(random_valueav),
    #     #         "time": str(datetime.now(timezone.utc))
    #     #     },
    #     #     "event": "avaibility",
    #     #     "timestamp": str(datetime.now(timezone.utc))
    #     # }
    #     # await nats_obj.publish_data(subject="avaibility.*", event_data=data_av)

    #     print("-----data published-----------")

    #     time.sleep(20)

    # await nc.publish("fpi.joe", b"hello")
    # await nc.publish("fpi.pam", b"hello")

    # msg = await sub.next_msg(timeout=0.1)
    # print(f"{msg.data} on subject {msg.subject}")

    # msg = await sub.next_msg(timeout=0.1)
    # print(f"{msg.data} on subject {msg.subject}")

    # await nc.publish("greet.bob", b"hello")
    # msg = await sub.next_msg(timeout=0.1)
    # print(f"{msg.data} on subject {msg.subject}")

    # await sub.unsubscribe()
    await nc.drain()

if __name__ == '__main__':
    while True:
        asyncio.run(main())
        print("data published")
        time.sleep(5)