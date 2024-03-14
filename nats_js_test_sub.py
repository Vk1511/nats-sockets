# import os
import asyncio
from nats_sdk.nats_js_sdk import NATSStream

async def main():
    notification_stream = "notification_fpi"
    subjects = ["notification_fpi.vishw", "notification_fpi.sachin"]

    nats_obj = await NATSStream.factory()

    if nats_obj:
        # await nats_obj.initiate_stream(
        #     stream_name=notification_stream,
        #     subjects=subjects,
        # )

        # await nats_obj.create_consumer(stream=notification_stream, subjects=subjects)

        event_data = {"name": "vishw"}
        ack = await nats_obj.publish_data(subject="notification_fpi.*", event_data=event_data)

        print("ack", ack)
        return ack
    else:
        print("NATS connection failed.")

if __name__ == '__main__':
    asyncio.run(main())