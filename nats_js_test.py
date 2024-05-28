# import os
import asyncio
from nats_sdk.nats_js_sdk import NATSStream

async def main():
    notification_stream = "notification_fpi"
    subjects = ["notification_fpi.vishw", "notification_fpi.sachin"]
    consumer = {
        "notification_fpi.vishw": "notification_fpi_vishw",
        "notification_fpi.sachin": "notification_fpi_sachin"
    }

    nats_obj = await NATSStream.factory()

    if nats_obj:
        await nats_obj.initiate_stream(
            stream_name=notification_stream,
            subjects=subjects,
        )

        await nats_obj.create_consumer(stream=notification_stream, subjects=consumer)

        event_data = {"name": "vishw111112222222"}
        ack = await nats_obj.publish_data(subject="notification_fpi.vishw", event_data=event_data, stream=notification_stream)
        # print("ack", dir(ack))
        # v = await ack.ack()
        # print('v',v)
        return ack
    else:
        print("NATS connection failed.")

if __name__ == '__main__':
    asyncio.run(main())
