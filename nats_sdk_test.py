from nats_sdk.nats_sdk import NATSStream
import asyncio
import time
from datetime import datetime, timezone
import random


async def test():
    nats_obj = await NATSStream.factory()

    while True:
        random_value = random.uniform(0.4, 0.5)
        data = {
            "data": {
                "fpi": str(random_value),
                "time": str(datetime.now(timezone.utc))
            },
            "event": "fpi",
            "timestamp": str(datetime.now(timezone.utc))
        }
        await nats_obj.publish_data(subject="fpi.*", event_data=data)

        # random_valueav = random.uniform(0.95, 1)
        # data_av = {
        #     "data": {
        #         "avaibility": str(random_valueav),
        #         "time": str(datetime.now(timezone.utc))
        #     },
        #     "event": "avaibility",
        #     "timestamp": str(datetime.now(timezone.utc))
        # }
        # await nats_obj.publish_data(subject="avaibility.*", event_data=data_av)

        print("-----data published-----------")

        time.sleep(20)

if __name__ == '__main__':
    asyncio.run(test())
